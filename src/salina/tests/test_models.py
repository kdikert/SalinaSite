

from django.test import TestCase
from salina.models import CMSText
from datetime import datetime


class TestCMSText(TestCase):
    
    def test_texts_are_ordered_by_default(self):
        CMSText.objects.create(text_id="t1", locale='en', timestamp=datetime(2012, 5, 1), text="text one")
        CMSText.objects.create(text_id="t1", locale='en', timestamp=datetime(2012, 5, 3), text="text three")
        CMSText.objects.create(text_id="t1", locale='en', timestamp=datetime(2012, 5, 2), text="text two")
        self.assertEqual(CMSText.objects.filter(text_id='t1')[0].text, "text three")

