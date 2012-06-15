

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


class TestCMSText(TestCase):
    
    def setUp(self):
        self.text = CMSText.objects.create(entry_id='test_text', description="desc")
    
    def test_unicode(self):
        self.assertEqual(str(self.text), "test_text")
    
    def test_get_translation_entries_per_locale_with_no_translations(self):
        entries = self.text.get_translation_entries_per_locale()
        
        self.assertTrue(isinstance(entries, list))
        self.assertEqual(len(entries), len(settings.LANGUAGES))
        for lang, text in entries:
            self.assertIsNotNone(lang)
            self.assertIsNone(text)
    
    def test_get_translation_entries_per_locale(self):
        self.text.overwrite_translation('en', "text en")
        self.text.overwrite_translation('nl', "text nl")
        
        entries = self.text.get_translation_entries_per_locale()
        
        entries = dict(e for e in entries)
        self.assertEqual(len(entries), len(settings.LANGUAGES))
        self.assertTrue(isinstance(entries['en'], CMSTranslation))
        self.assertEqual(entries['en'].text, "text en")
        self.assertEqual(entries['nl'].text, "text nl")
    
    def test_update_translation_adds_new_text_if_time_limit_exceeded(self):
        self.text.overwrite_translation('en', "text en", update_time=datetime(2012, 1, 6, 0, 0))
        
        self.text.update_translation('en', "updated en", update_time=datetime(2012, 1, 7, 0, 0))
        
        translations = list(self.text.translations.all())
        self.assertEqual(len(translations), 2)
        self.assertEqual(translations[0].timestamp, datetime(2012, 1, 7, 0, 0))
        self.assertEqual(translations[0].text, "updated en")
        self.assertEqual(translations[1].timestamp, datetime(2012, 1, 6, 0, 0))
        self.assertEqual(translations[1].text, "text en")
    
    def test_update_translation_amends_if_within_time_limit(self):
        self.text.overwrite_translation('en', "text en", update_time=datetime(2012, 1, 6, 0, 0))
        
        self.text.update_translation('en', "updated en", update_time=datetime(2012, 1, 6, 0, 1))

        translation = self.text.translations.get()
        self.assertEqual(translation.timestamp, datetime(2012, 1, 6, 0, 1))
        self.assertEqual(translation.text, "updated en")
    
    def test_overwrite_translation_deletes_old_translations(self):
        self.text.update_translation('en', "en 1", update_time=datetime(2012, 1, 6, 0, 0))
        self.text.update_translation('en', "en 2", update_time=datetime(2012, 1, 7, 0, 0))
        self.assertEqual(self.text.translations.count(), 2)
        
        self.text.overwrite_translation('en', "text en", update_time=datetime(2012, 1, 8, 0, 0))
        
        self.assertEqual(self.text.translations.count(), 1)
        translation = self.text.translations.get()
        self.assertEqual(translation.timestamp, datetime(2012, 1, 8, 0, 0))
        self.assertEqual(translation.text, "text en")
    
    def test_get_translation_gets_latest_version_of_text(self):
        self.text.translations.create(locale='en', text="en 1", timestamp=datetime(2012, 1, 6, 0, 0))
        self.text.translations.create(locale='en', text="en 2", timestamp=datetime(2012, 1, 8, 0, 0))
        self.text.translations.create(locale='en', text="en 3", timestamp=datetime(2012, 1, 7, 0, 0))
        
        text = self.text.get_current_translation()
        
        self.assertEqual(text, "en 2")

