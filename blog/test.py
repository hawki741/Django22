from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import Post

class TestView(TestCase):

    def setUp(self): # test 전에 공통적으로 실행되는 작업
        self.client = Client() # 서버구동 없이 내부적으로 실행된 client 화면 정보를 가짐

    def test_post_list(self):
        response = self.client.get('/blog/') # url : IP주소/blog/
        # response 결과가 정상적으로 왔는지
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, 'html.parser')
        # title이 정상적으로 보이는지
        self.assertEqual(soup.title.text, 'Blog')
        # navbar가 정상적으로 보이는지
        navbar = soup.nav
        self.assertIn('Blog', navbar.text)
        self.assertIn('About Me', navbar.text)

        # post가 정상적으로 보이는지
        #1 맨 처음엔 포스트가 하나도 없음
        self.assertEqual(Post.objects.count(),0)
        main_area = soup.find('div', id='main-area')
        self.assertIn('아직 게시물이 없습니다.', main_area.text)

        #2 포스트 추가
        post_001 = Post.objects.create(title="첫번째 포스트",content="첫번째 포스트입니다")
        post_002 = Post.objects.create(title="두번째 포스트", content="두번째 포스트입니다")
        self.assertEqual(Post.objects.count(), 2)

        response = self.client.get('/blog/') # 포스트 추가 후 다시 접속
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        main_area = soup.find('div', id='main-area')
        self.assertIn(post_001.title, main_area.text)
        self.assertIn(post_002.title, main_area.text)
        self.assertNotIn('아직 게시물이 없습니다.', main_area.text)