from products.models import ProductCategory, Product
from tools.product_generation.definitions import PATH_TO_CATEGORIES_FOR_DB, PATH_TO_GOODS_FOR_DB
from tools.product_generation.utils import read_json


def clear_db():
    """Clearing the database before creating"""
    ProductCategory.objects.all().delete()
    Product.objects.all().delete()


def write_to_db_categories(categories: list[dict[str, str]]):
    """Filling the database with fake data"""

    for category in categories:
        ProductCategory.objects.create(name=category['name'],
                                       description=category['description'])


def write_to_db_products(goods: list[dict[str, str]]):
    """Filling the database with fake data"""

    for product in goods:
        category_id = ProductCategory.objects.filter(name=product['category']).first()
        Product.objects.create(name=product['name'],
                               description=product['description'],
                               price=float(product['price']),
                               quantity=product['quantity'],
                               image=product['image'],
                               category=category_id,
                               )


def main():
    clear_db()

    categories = read_json(PATH_TO_CATEGORIES_FOR_DB)
    write_to_db_categories(categories)

    goods = read_json(PATH_TO_GOODS_FOR_DB)
    write_to_db_products(goods)
