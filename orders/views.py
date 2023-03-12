from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from common.views import TitleMixin


class OrderCreateView(TitleMixin, TemplateView):
    template_name = 'orders/order-create.html'
    success_url = reverse_lazy('orders:order_create')
    title = 'Store - Checkout'
