

from datetime import datetime

from django.test import TestCase

from salina.models import *   #@UnusedWildImport


class TestProductGroup(TestCase):
    
    def test_create_creates_cms_text(self):
        self.assertEqual(CMSText.objects.all().count(), 0)
        
        product_group = ProductGroup.objects.create("test_group")
        
        self.assertIsNotNone(product_group.name_text)
        self.assertEqual(CMSText.objects.all().count(), 1)
        
        text = CMSText.objects.get()
        self.assertEqual(text.entry_id, "product_group_test_group")
    
    def test_delete_removes_cms_text(self):
        CMSText.objects.create(entry_id='unrelated_entry', description='')
        product_group = ProductGroup.objects.create("test_group")
        self.assertIsNotNone(product_group.name_text)
        self.assertEqual(CMSText.objects.all().count(), 2)
        
        product_group.delete()
        
        self.assertEqual(CMSText.objects.all().count(), 1)
        text = CMSText.objects.get()
        self.assertEqual(text.entry_id, "unrelated_entry")


class TestProduct(TestCase):
    
    def setUp(self):
        self.product_group = ProductGroup.objects.create("test_group")
    
    def test_create_creates_cms_text(self):
        self.assertEqual(CMSText.objects.all().count(), 1)
        
        product = Product.objects.create("product1", self.product_group)
        
        self.assertIsNotNone(product.name_text)
        self.assertEqual(CMSText.objects.all().count(), 2)
        
        CMSText.objects.get(entry_id="product_product1")
    
    def test_delete_removes_cms_text(self):
        CMSText.objects.create(entry_id='unrelated_entry', description='')
        product = Product.objects.create("product1", self.product_group)
        
        self.assertEqual(CMSText.objects.all().count(), 3)
        self.assertEqual(CMSText.objects.filter(entry_id="product_product1").count(), 1)
        
        product.delete()
        
        self.assertEqual(CMSText.objects.all().count(), 2)
        self.assertEqual(CMSText.objects.filter(entry_id="product_product1").count(), 0)


#class TestCMSText(TestCase):
#    
#    def test_texts_are_ordered_by_default(self):
#        CMSText.objects.create(text_id="t1", locale='en', timestamp=datetime(2012, 5, 1), text="text one")
#        CMSText.objects.create(text_id="t1", locale='en', timestamp=datetime(2012, 5, 3), text="text three")
#        CMSText.objects.create(text_id="t1", locale='en', timestamp=datetime(2012, 5, 2), text="text two")
#        self.assertEqual(CMSText.objects.filter(text_id='t1')[0].text, "text three")

