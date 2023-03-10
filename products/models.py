from django.db import models
from django.urls import reverse_lazy
from django.utils import timezone

from users.models import User


class ProductCategory(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=False)  # disable auto increment
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class PublishManager(models.Manager):
    def get_queryset(self):
        return super(PublishManager, self).get_queryset().filter(status='published')


class Product(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published')
    )
    id = models.IntegerField(primary_key=True, auto_created=False)  # disable auto increment
    name = models.CharField(max_length=256)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products_images', null=True, blank=True)
    category = models.ForeignKey(to=ProductCategory, on_delete=models.CASCADE)

    publish = models.DateTimeField(default=timezone.localtime)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='published')

    objects = models.Manager()
    published = PublishManager()

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'
        ordering = ('-publish', '-created')

    def __str__(self):
        return f'Product: {self.name} | Category: {self.category.name}'

    def get_absolute_url(self):
        return reverse_lazy('products:product_details',
                            args=[self.pk, ])

    def likes_count(self):
        return self.likes.count()

    def is_liked_by(self, user):
        return self.likes.filter(user=user).exists()


class PostLike(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_likes')

    class Meta:
        unique_together = ('product', 'user')


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    body = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('-updated', '-created')

    def __str__(self):
        return f'Comment by {self.author.username} - {self.body}'

    def likes_count(self):
        return self.likes.count()

    def is_liked_by(self, user):
        return self.likes.filter(user=user).exists()


class CommentLike(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_likes')

    class Meta:
        unique_together = ('comment', 'user')


class BasketQuerySet(models.QuerySet):
    def total_sum(self):
        return sum(basket.sum() for basket in self)

    def total_quantity(self):
        return sum(basket.quantity for basket in self)


class Basket(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    objects = BasketQuerySet.as_manager()

    def __str__(self):
        return f'Basket for {self.user.username} | Product: {self.product.name}'

    def sum(self):
        return self.product.price * self.quantity


"""
on_delete=models.CASCADE - delete all
on_delete=models.PROTECT - you cannot delete a category until all products belonging to this category have been deleted
on_delete=models.SET_DEFAULT, default='...' - when deleted, the default value will be set
"""
