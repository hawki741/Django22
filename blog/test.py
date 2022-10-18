from django.test import TestCase, Client
from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from .models import Post

class TestView(TestCase):

    def setUp(self): # test 전에 공통적으로 실행되는 작업
        self.client = Client() # 서버구동 없이 내부적으로 실행된 client 화면 정보를 가짐
        self.user_001 = User.objects.create_user(username='kim', password='somepassword')
        self.user_002 = User.objects.create_user(username='lee', password='somepassword')

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

    def test_post_list(self):
        response = self.client.get('/blog/') # url : IP주소/blog/
        # response 결과가 정상적으로 왔는지
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, 'html.parser')
        # title이 정상적으로 보이는지
        self.assertEqual(soup.title.text, 'Blog')
        # navbar가 정상적으로 보이는지
        self.nav_test(soup)

        # post가 정상적으로 보이는지
        #1 맨 처음엔 포스트가 하나도 없음
        self.assertEqual(Post.objects.count(),0)
        main_area = soup.find('div', id='main-area')
        self.assertIn('아직 게시물이 없습니다.', main_area.text)

        #2 포스트 추가
        post_001 = Post.objects.create(title="첫번째 포스트", content="첫번째 포스트입니다",
                                       author=self.user_001)
        post_002 = Post.objects.create(title="두번째 포스트", content="두번째 포스트입니다",
                                       author=self.user_002)
        self.assertEqual(Post.objects.count(), 2)

        response = self.client.get('/blog/') # 포스트 추가 후 다시 접속
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        main_area = soup.find('div', id='main-area')
        self.assertIn(post_001.title, main_area.text)
        self.assertIn(post_002.title, main_area.text)
        self.assertNotIn('아직 게시물이 없습니다.', main_area.text)

        self.assertIn(self.user_001.username.upper(), main_area.text)
        self.assertIn(self.user_002.username.upper(), main_area.text)

    def test_post_detail(self):
        post_001 = Post.objects.create(title="첫번째 포스트", content="첫번째 포스트입니다",
                                       author=self.user_001)
        self.assertEqual(post_001.get_absolute_url(), '/blog/1/')

        response = self.client.get(post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        self.nav_test(soup)

        self.assertIn(post_001.title, soup.title.text)

        # post_detail에 amin_area, post_area 추가
        main_area = soup.find('div', id='main-area')
        post_area = main_area.find('div', id='post-area')
        self.assertIn(post_001.title, post_area.text)
        self.assertIn(post_001.content, post_area.text)
        self.assertIn(self.user_001.username.upper(), post_area.text)