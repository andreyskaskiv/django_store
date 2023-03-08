from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.views.generic import DetailView
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

from common.views import TitleMixin
from products.models import Product, ProductCategory, Basket


class IndexView(TitleMixin, TemplateView):
    template_name = 'products/index.html'
    title = 'Store'


class ProductsListView(TitleMixin, ListView):
    model = Product
    template_name = 'products/products.html'
    paginate_by = 9
    title = 'Store - Catalog'

    def get_queryset(self):
        queryset = super(ProductsListView, self).get_queryset()  # Product.objects.all()
        queryset = queryset.order_by('id')

        category_id = self.kwargs.get('category_id')  # None
        return queryset.filter(category_id=category_id) if category_id else queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductsListView, self).get_context_data()

        context['categories'] = ProductCategory.objects.all()
        return context


class ProductDetailView(TitleMixin, DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    title = 'Store - Product details'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductDetailView, self).get_context_data()

        context['categories'] = ProductCategory.objects.all()
        return context


@login_required
def basket_add(request, product_id):
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)

    if not baskets.exists():
        Basket.objects.create(user=request.user, product_id=product_id, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
