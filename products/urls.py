from django.urls import path

from products.views import ProductsListView, ProductDetailView, basket_add, basket_remove

app_name = 'products'

urlpatterns = [
    path('', ProductsListView.as_view(), name='index'),
    path('category/<int:category_id>/', ProductsListView.as_view(), name='category'),
    path('product_details/<int:pk>/', ProductDetailView.as_view(), name='product_details'),
    path('page/<int:page>/', ProductsListView.as_view(), name='paginator'),

    path('baskets/add/<int:product_id>/', basket_add, name='basket_add'),
    path('baskets/remove/<int:basket_id>/', basket_remove, name='basket_remove'),
]
