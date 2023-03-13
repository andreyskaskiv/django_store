from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import DetailView
from django.views.generic.base import TemplateView, View
from django.views.generic.list import ListView

from common.views import TitleMixin
from products.forms import CommentForm
from products.models import Product, ProductCategory, Basket, Comment, CommentLike, ProductLike


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
    queryset = Product.published.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)

        context['form'] = CommentForm(initial={'product': self.object})
        context['categories'] = ProductCategory.objects.all()
        return context

    @method_decorator(login_required, name='dispatch')
    def post(self, request, *args, **kwargs):
        post_comment = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = Comment(body=request.POST.get('body'),
                                  author=self.request.user,
                                  product=self.get_object())
            new_comment.save()
            return HttpResponseRedirect(f'{post_comment.get_absolute_url()}')
        return self.render_to_response({'product': post_comment, 'form': form})


class CommentLikeView(LoginRequiredMixin, View):
    def get(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        comment_like, created = CommentLike.objects.get_or_create(comment=comment, user=request.user)
        if not created:
            comment_like.delete()
        return HttpResponseRedirect(f'{comment.product.get_absolute_url()}')


class ProductLikeView(LoginRequiredMixin, View):
    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        product_like, created = ProductLike.objects.get_or_create(product=product, user=request.user)
        if not created:
            product_like.delete()
        return HttpResponseRedirect(reverse_lazy('products:index'))


class CommentLikeAdminView(LoginRequiredMixin, View):
    def get(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)

        if not request.user.is_superuser:
            raise PermissionDenied("You don't have permission to admin comments")

        comment.active = False if comment.active else True
        comment.save()
        return HttpResponseRedirect(f'{comment.product.get_absolute_url()}')


class CommentDeleteAdminView(LoginRequiredMixin, View):
    model = Comment

    def get(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        if not request.user.is_superuser:
            raise PermissionDenied("You don't have permission to admin comments")
        comment.delete()
        return HttpResponseRedirect(f'{comment.product.get_absolute_url()}')


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
