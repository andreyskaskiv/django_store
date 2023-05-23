from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from products.models import Product, ProductCategory


class IndexViewTestCase(TestCase):

    def test_01_view(self):
        path = reverse('index')
        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Store')
        self.assertTemplateUsed(response, 'products/index.html')


class ProductsListViewTestCase(TestCase):
    fixtures = ['categories.json', 'goods.json']

    def setUp(self):
        self.products = Product.objects.all().order_by('id')

    def test_01_list(self):
        path = reverse('products:index')
        response = self.client.get(path)

        self._common_tests(response)
        # print(list(response.context_data['object_list']))
        # print(list(self.products[:9]))

        self.assertEqual(list(response.context_data['object_list']), list(self.products[:9]))  # == paginate_by = 9

    def test_02_list_with_category(self):
        category = ProductCategory.objects.first()
        path = reverse('products:category', kwargs={
            'category_id': category.id})  # path('category/<int:category_id>/', ProductsListView.as_view(), name='category'),
        response = self.client.get(path)

        self._common_tests(response)

        # print(list(response.context_data['object_list']))
        # print(list(self.products.filter(category_id=category.id))[:9])  # == paginate_by = 9

        self.assertEqual(
            list(response.context_data['object_list']),
            list(self.products.filter(category_id=category.id))[:9] # == paginate_by = 9
        )

    def _common_tests(self, response):
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Store - Catalog')
        self.assertTemplateUsed(response, 'products/products.html')


class ProductDetailViewTestCase(TestCase):
    fixtures = ['categories.json', 'goods.json']

    def test_01_view(self):
        products = Product.objects.first()  # id = 1

        path = reverse('products:product_details', kwargs={
            'pk': products.id})  # path('product_details/<int:pk>/', ProductDetailView.as_view(), name='product_details'),
        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, '<title>Store - Product details</title>')
        self.assertEqual(response.context_data['title'], 'Store - Product details')
        self.assertTemplateUsed(response, 'products/product_detail.html')
