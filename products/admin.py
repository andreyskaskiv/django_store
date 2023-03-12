from django.contrib import admin

from products.models import Basket, Product, ProductCategory, Comment, CommentLike

admin.site.register(ProductCategory)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """How and what will be reflected in the admin panel"""

    list_display = ('name', 'price', 'quantity', 'category', 'publish', 'status')
    fields = ('image', 'name', 'description', ('price', 'quantity'), 'stripe_product_price_id', 'category', 'status', 'publish')
    list_filter = ('status', 'created', 'publish')
    # readonly_fields = ('description',)
    search_fields = ('name',)
    ordering = ('-name', '-price', '-quantity',)


class BasketAdmin(admin.TabularInline):
    model = Basket
    fields = ('product', 'quantity', 'created_timestamp')
    readonly_fields = ('created_timestamp',)
    extra = 0


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('product', 'author', 'created', 'active')
    list_filter = ('active', 'created')
    search_fields = ('body',)


@admin.register(CommentLike)
class CommentLikeAdmin(admin.ModelAdmin):
    list_display = ('comment', 'user')
    search_fields = ('user__username',)