from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

from products.models import Product, ProductCategory, Basket


def index(request):
    context = {'title': 'Store'}
    return render(request,
                  'products/index.html',
                  context)


def products(request, category_id=None):
    products = Product.objects.filter(category_id=category_id) if category_id else Product.objects.all()

    context = {
        'title': 'Store - Catalog',
        'categories': ProductCategory.objects.all(),
        'products': products
    }
    return render(request,
                  'products/products.html',
                  context)


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
