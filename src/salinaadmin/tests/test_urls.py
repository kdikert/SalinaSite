

from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from .. import views


class TestLogin(TestCase):
    
    def test_get_returns_template(self):
        response = self.client.get(reverse(views.login))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'salinaadmin/login.html')
    
    def test_successful_log_in_redirects_to_admin_page(self):
        User.objects.create_superuser("tester", "test@test.com", "p4ss")
        
        response = self.client.post(reverse(views.login), data={'username':"tester", 'password':"p4ss"})
        self.assertEqual(response.status_code, 302)
    
    def test_log_in_with_authenticated_user_redirects_to_admin_page(self):
        User.objects.create_superuser("tester", "test@test.com", "p4ss")
        self.client.login(username="tester", password="p4ss")
        
        response = self.client.get(reverse(views.login))
        self.assertEqual(response.status_code, 302)
