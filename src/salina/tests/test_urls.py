
from django.test import TestCase


class TestIndex(TestCase):
    urls = __name__.rsplit('.', 1)[0] + '.urls'
    
    def test_get_returns_200(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_correct_template_used(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'salina/index.html')
