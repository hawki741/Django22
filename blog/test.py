from django.test import TestCase, Client
from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from .models import Post, Category

class TestView(TestCase):

    def setUp(self): # test 전에 공통적으로 실행되는 작업
        self.client = Client() # 서버구동 없이 내부적으로 실행된 client 화면 정보를 가짐

        self.user_001 = User.objects.create_user(username='kim', password='somepassword')
        self.user_002 = User.objects.create_user(username='lee', password='somepassword')

        self.category_com = Category.objects.create(name='computer',slug='computer')
        self.category_edu = Category.objects.create(name='education',slug='education')

        self.post_001 = Post.objects.create(title="첫번째 포스트", content="첫번째 포스트입니다",
                                       author=self.user_001,
                                       category=self.category_com)
        self.post_002 = Post.objects.create(title="두번째 포스트", content="두번째 포스트입니다",
                                       author=self.user_002,
                                       category=self.category_edu)
        self.post_003 = Post.objects.create(title="세번째 포스트", content="세번째 포스트입니다",
                                       author=self.user_002)

    def nav_test(self, soup):
        navbar = soup.nav
        self.assertIn('Blog', navbar.text)
        self.assertIn('About Me', navbar.text)

        logo_btn = navbar.find('a', text="InternetProgramming")
        self.assertEqual(logo_btn.attrs['href'], '/')
        home_btn = navbar.find('a', text="Home")
        self.assertEqual(home_btn.attrs['href'], '/')
        blog_btn = navbar.find('a', text="Blog")
        self.assertEqual(blog_btn.attrs['href'], '/blog/')
        about_btn = navbar.find('a', text="About Me")
        self.assertEqual(about_btn.attrs['href'], '/about_me/')

    def category_test(self, soup):
        category_card = soup.find('div', id='category_card')
        self.assertIn('Categories', category_card.text)
        self.assertIn(f'{self.category_com.name} ({self.category_com.post_set.count()})', category_card.text)
        self.assertIn(f'{self.category_edu.name} ({self.category_edu.post_set.count()})', category_card.text)
        self.assertIn(f'미분류 (1)', category_card.text)

    def test_post_list(self):
        #2 포스트 추가

        self.assertEqual(Post.objects.count(), 3)

        response = self.client.get('/blog/') # 포스트 추가 후 다시 접속
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        self.nav_test(soup)
        self.category_test(soup)

        main_area = soup.find('div', id='main-area')
        self.assertNotIn('아직 게시물이 없습니다.', main_area.text)

        post_001_card = main_area.find('div', id='post-1')
        self.assertIn(self.post_001.title, post_001_card.text)
        self.assertIn(self.post_001.category.name, post_001_card.text)

        post_002_card = main_area.find('div', id='post-2')
        self.assertIn(self.post_002.title, post_002_card.text)
        self.assertIn(self.post_002.category.name, post_002_card.text)

        post_003_card = main_area.find('div', id='post-3')
        self.assertIn(self.post_003.title, post_003_card.text)
        self.assertIn('미분류', post_003_card.text)

        self.assertIn(self.user_001.username.upper(), main_area.text)
        self.assertIn(self.user_002.username.upper(), main_area.text)

        # Post가 없을 때
        Post.objects.all().delete()
        self.assertEqual(Post.objects.count(), 0)
        response = self.client.get('/blog/')  # url : IP주소/blog/
        # response 결과가 정상적으로 왔는지
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, 'html.parser')

        # title이 정상적으로 보이는지
        self.assertEqual(soup.title.text, 'Blog')
        # navbar가 정상적으로 보이는지
        self.nav_test(soup)

        # post가 정상적으로 보이는지
        # 1 맨 처음엔 포스트가 하나도 없음
        self.assertEqual(Post.objects.count(), 0)
        main_area = soup.find('div', id='main-area')
        self.assertIn('아직 게시물이 없습니다.', main_area.text)

    def test_post_detail(self):
        #post_001 = Post.objects.create(title="첫번째 포스트", content="첫번째 포스트입니다",
        #                               author=self.user_001)
        self.assertEqual(self.post_001.get_absolute_url(), '/blog/1/')

        response = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        self.nav_test(soup)
        self.category_test(soup)

        self.assertIn(self.post_001.title, soup.title.text)

        # post_detail에 amin_area, post_area 추가
        main_area = soup.find('div', id='main-area')
        post_area = main_area.find('div', id='post-area')
        self.assertIn(self.post_001.title, post_area.text)
        self.assertIn(self.post_001.content, post_area.text)
        self.assertIn(self.user_001.username.upper(), post_area.text)
        self.assertIn(self.post_001.category.name, post_area.text)