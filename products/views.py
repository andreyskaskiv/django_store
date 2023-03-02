from django.shortcuts import render


def index(request):
    context = {'title': 'Store'}
    return render(request,
                  'products/index.html',
                  context)


def products(request):
    context = {
        'title': 'Store - Catalog',
        'products': [
            {
                'image': '/static/vendor/img/products/Adidas-hoodie.png',
                'name': 'adidas Originals Black Monogram Hoodie',
                'price': 100,
                'description': 'Soft fabric for sweatshirts. Style and comfort is a way of life.'
            },
            {
                'image': '/static/vendor/img/products/Blue-jacket-The-North-Face.png',
                'name': 'The North Face blue jacket',
                'price': 200,
                'description': 'Smooth fabric. Waterproof coating. Lightweight and warm down fill.'
            },
            {
                'image': '/static/vendor/img/products/Brown-sports-oversized-top-ASOS-DESIGN.png',
                'name': 'Nike Black Heritage Backpack',
                'price': 300,
                'description': 'Plush material. Comfortable and soft.'
            },
            {
                'image': '/static/vendor/img/products/Black-Dr-Martens-shoes.png',
                'name': 'Dr Martens 1461 Bex Black 3-Eye Platform Shoes',
                'price': 400,
                'description': 'Smooth leather upper. Natural material.'
            },
        ]
    }
    return render(request,
                  'products/products.html',
                  context)
