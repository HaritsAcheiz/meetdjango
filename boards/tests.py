from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse, resolve

from boards.models import Board, Topic, Post
from boards.views import home, board_topics, new_topic


# Create your tests here.
class HomeTests(TestCase):
    def test_home_views_status_code(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func, home)

class BoardTopicsTests(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name='Django', description='Django board')

    def test_board_topics_view_success_status_code(self):
        url = reverse('board_topics', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_board_topics_view_success_not_found_code(self):
        url = reverse('board_topics', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_board_topics_url_resolves_board_topics_view(self):
        view = resolve('/boards/1/')
        self.assertEquals(view.func, board_topics)

    def test_home_view_contains_link_to_topic_page(self):
        homepage_url = reverse('home')
        board_topics_url = reverse('board_topics', kwargs={'pk': self.board.pk})
        response = self.client.get(homepage_url)
        self.assertContains(response, f'href="{board_topics_url}"')

    def test_board_topics_view_contains_required_navigation_link(self):
        board_topics_url = reverse('board_topics', kwargs={'pk': 1})
        homepage_url = reverse('home')
        new_topic_url = reverse('new_topic', kwargs={'pk': 1})
        response = self.client.get(board_topics_url)
        self.assertContains(response, f'href="{homepage_url}"')
        self.assertContains(response, f'href="{new_topic_url}"')

class NewTopicTests(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name='Django', description='Django Board')
        self.user = User.objects.create_user(username='john', email='john@doe.com', password='123')

    def test_csrf(self):
        url = reverse('new_topic', kwargs={'pk':1})
        response = self.client.get(url)
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_new_topic_valid_post_data(self):
        url = reverse('new_topic', kwargs={'pk': 1})
        data = {
            'subject': 'Test title',
            'message': 'Test message'
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, 302)
        self.assertTrue(Topic.objects.exists())
        self.assertTrue(Post.objects.exists())

    def test_new_topic_invalid_post_data(self):
        url = reverse('new_topic', kwargs={'pk': 1})
        response = self.client.post(url, {})
        self.assertEquals(response.status_code, 200)

    def test_new_topic_invalid_post_empty_data(self):
        url = reverse('new_topic', kwargs={'pk': 1})
        data = {
            'subject': '',
            'message': ''
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, 200)
        self.assertTrue(Topic.objects.exists())
        self.assertTrue(Post.objects.exists())

    def test_new_topic_view_success_status_code(self):
        url = reverse('new_topic', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_new_topic_view_not_found_status_code(self):
        url = reverse('new_topic', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_new_topic_url_resolve_new_topic_function(self):
        view = resolve('/boards/1/new/')
        self.assertEquals(view.func, new_topic)

    def test_new_topic_view_contain_required_navigation_link(self):
        new_topic_url = reverse('new_topic', kwargs={'pk':1})
        board_topic_url = reverse('board_topics', kwargs={'pk':1})
        homepage_url = reverse('home')
        response = self.client.get(new_topic_url)
        self.assertContains(response, f'href="{board_topic_url}"')
        self.assertContains(response, f'href="{homepage_url}"')
