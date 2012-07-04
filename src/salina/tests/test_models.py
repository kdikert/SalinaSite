

from django.test import TestCase

from salina.models import *   #@UnusedWildImport


class TestMaterial(TestCase):
    
    def test_create_creates_cms_text(self):
        self.assertEqual(CMSText.objects.all().count(), 0)
        
        material = Material.objects.create(material_id="mat1")
        
        self.assertIsNotNone(material.name_text)
        self.assertEqual(CMSText.objects.all().count(), 1)
        
        self.assertEqual(CMSText.objects.filter(entry_id="material-mat1").count(), 1)
    
    def test_delete_removes_cms_text(self):
        CMSText.objects.create(entry_id='unrelated_entry', description='')
        material = Material.objects.create(material_id="mat1")
        
        self.assertEqual(CMSText.objects.all().count(), 2)
        self.assertEqual(CMSText.objects.filter(entry_id="material-mat1").count(), 1)
        
        material.delete()
        
        self.assertEqual(CMSText.objects.all().count(), 1)
        self.assertEqual(CMSText.objects.filter(entry_id="material-mat1").count(), 0)


class TestProductGroup(TestCase):
    
    def test_create_creates_cms_text(self):
        self.assertEqual(CMSText.objects.all().count(), 0)
        
        product_group = ProductGroup.objects.create(group_id="test_group")
        
        self.assertIsNotNone(product_group.name_text)
        self.assertEqual(CMSText.objects.all().count(), 1)
        
        text = CMSText.objects.get()
        self.assertEqual(text.entry_id, "productgroup-test_group")
    
    def test_delete_removes_cms_text(self):
        CMSText.objects.create(entry_id='unrelated_entry', description='')
        product_group = ProductGroup.objects.create(group_id="test_group")
        self.assertIsNotNone(product_group.name_text)
        self.assertEqual(CMSText.objects.all().count(), 2)
        
        product_group.delete()
        
        self.assertEqual(CMSText.objects.all().count(), 1)
        text = CMSText.objects.get()
        self.assertEqual(text.entry_id, "unrelated_entry")


class TestProduct(TestCase):
    
    def setUp(self):
        self.product_group = ProductGroup.objects.create(group_id="test_group")
    
    def test_create_creates_cms_text(self):
        self.assertEqual(CMSText.objects.all().count(), 1)
        
        product = Product.objects.create(product_id="product1",
                                         product_group=self.product_group)
        
        self.assertIsNotNone(product.name_text)
        self.assertEqual(CMSText.objects.all().count(), 2)
        
        self.assertEqual(CMSText.objects.filter(entry_id="product-product1").count(), 1)
    
    def test_delete_removes_cms_text(self):
        CMSText.objects.create(entry_id='unrelated_entry', description='')
        product = Product.objects.create(product_id="product1",
                                         product_group=self.product_group)
        
        self.assertEqual(CMSText.objects.all().count(), 3)
        self.assertEqual(CMSText.objects.filter(entry_id="product-product1").count(), 1)
        
        product.delete()
        
        self.assertEqual(CMSText.objects.all().count(), 2)
        self.assertEqual(CMSText.objects.filter(entry_id="product_product1").count(), 0)
    
    def test_get_total_price_with_no_product_parts(self):
        product = Product.objects.create(product_id="product1", product_group=self.product_group)
        self.assertEqual(product.get_total_price(), 0)
    
    def test_get_total_price(self):
        product = Product.objects.create(product_id="product1", product_group=self.product_group)
        ProductPart.objects.create(product=product, time_min=30, price=5)
        ProductPart.objects.create(product=product, time_min=30, price=7)
        
        self.assertEqual(product.get_total_price(), 12)
    
    def test_get_total_time_with_no_product_parts(self):
        product = Product.objects.create(product_id="product1", product_group=self.product_group)
        self.assertEqual(product.get_total_time(), 0)
    
    def test_get_total_time(self):
        product = Product.objects.create(product_id="product1", product_group=self.product_group)
        ProductPart.objects.create(product=product, time_min=30, price=5)
        ProductPart.objects.create(product=product, time_min=60, price=5)
        
        self.assertEqual(product.get_total_time(), 90)


class TestProductPartColumn(TestCase):
    
    def setUp(self):
        self.product_group = ProductGroup.objects.create(group_id="test_group")
        self.product = Product.objects.create(product_id="product1",
                                              product_group=self.product_group)
        self.mat_yarn = Material.objects.create(material_id="yarn")
        self.mat_fabric = Material.objects.create(material_id="fabric")
        self.mat_other = Material.objects.create(material_id="other")
        
        MaterialColumn.objects.create(product=self.product, material=self.mat_fabric)
        MaterialColumn.objects.create(product=self.product, material=self.mat_yarn)
        MaterialColumn.objects.create(product=self.product, material=self.mat_other)
        
        self.part = ProductPart.objects.create(product=self.product, time_min=30, price=5)
    
    def test_create_creates_cms_text(self):
        self.assertEqual(CMSText.objects.all().count(), 6)
        
        product_part_column = ProductPartColumn.objects.create(material_column=self.product.material_columns.all()[0],
                                                               product_part=self.part,
                                                               amount="10")
        
        self.assertIsNotNone(product_part_column.text)
        self.assertEqual(CMSText.objects.all().count(), 7)
        
        self.assertEqual(CMSText.objects.filter(entry_id="productpartcolumn-0").count(), 1)
    
    def test_delete_removes_cms_text(self):
        
        product_part_column = ProductPartColumn.objects.create(material_column=self.product.material_columns.all()[0],
                                                               product_part=self.part,
                                                               amount="10")
        
        self.assertEqual(CMSText.objects.all().count(), 7)
        self.assertEqual(CMSText.objects.filter(entry_id="productpartcolumn-0").count(), 1)
        
        product_part_column.delete()
        
        self.assertEqual(CMSText.objects.all().count(), 6)
        self.assertEqual(CMSText.objects.filter(entry_id="productpartcolumn-0").count(), 0)
    
    def test_ordering(self):
        
        for material_column in self.product.material_columns.all():
            ProductPartColumn.objects.create(material_column=material_column,
                                             product_part=self.part)
        
        columns = list(self.part.columns.all())
        self.assertEqual(columns[0].material_column.material.material_id, "fabric")
        self.assertEqual(columns[1].material_column.material.material_id, "yarn")
        self.assertEqual(columns[2].material_column.material.material_id, "other")
        
        self.product.set_materialcolumn_order([2, 1, 3])
        
        columns = list(self.part.columns.all())
        self.assertEqual(columns[0].material_column.material.material_id, "yarn")
        self.assertEqual(columns[1].material_column.material.material_id, "fabric")
        self.assertEqual(columns[2].material_column.material.material_id, "other")


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
    
    def test_update_translation_ignores_identical_text(self):
        self.text.overwrite_translation('en', "text en", update_time=datetime(2012, 1, 6, 0, 0))
        self.assertEqual(self.text.translations.count(), 1)
        
        self.text.update_translation('en', "text en", update_time=datetime(2012, 1, 7, 0, 0))
        
        translation = self.text.translations.get()
        self.assertEqual(translation.timestamp, datetime(2012, 1, 6, 0, 0))
        self.assertEqual(translation.text, "text en")
    
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

