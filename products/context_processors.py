from products.models import Basket, ProductLike


def baskets(request):
    user = request.user
    return {'baskets': Basket.objects.filter(user=user) if user.is_authenticated else []}


def likes(request):
    user = request.user
    return {'likes': ProductLike.objects.filter(user=user) if user.is_authenticated else []}