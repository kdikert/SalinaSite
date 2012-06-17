
from django.test import TestCase
from django.core.urlresolvers import reverse

from .. import views


class TestIndex(TestCase):
    
    def setUp(self):
        self.url = reverse('index')
    
    def test_get_returns_200(self):
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'salina/index.html')


class TestAtelier(TestCase):
    
    def setUp(self):
        self.url = reverse(views.atelier)
    
    def test_get_returns_200(self):
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'salina/atelier.html')

