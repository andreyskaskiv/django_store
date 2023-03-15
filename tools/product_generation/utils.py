import json
import random
import re

categories = ('Dress', 'Top', 'Slacks', 'Jumpsuit', 'Jeans', 'Jacket', 'Sweatshirt', 'Skirt', 'Joggers', 'Others')


def read_json(path_to_file):
    with open(path_to_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


def prepare_categories(categories: list[str]):
    """ Fetching data  to write to jason """
    categories_to_json = []
    for categorie in categories:
        temp = {
            'name': categorie,
            'description': '',
        }
        categories_to_json.append(temp)
    return categories_to_json


def is_digit(value: str):
    return re.search(r'\d+\.\d+', value).group()


def product_category(product_name: str, categories):
    for category in categories:
        if category in product_name:
            return category
    return 'Others'


def prepare_goods(goods: list[dict[str, str]]):
    """ Fetching data  to write to jason """
    goods_to_json = []
    for product in goods:
        temp = {
            "name": product['name'],
            "description": product['description'],
            "price": is_digit(product['price']),
            "quantity": random.randint(5, 15),
            "image": product['url_img'],
            "category": product_category(product['name'], categories)
        }
        goods_to_json.append(temp)
    return goods_to_json


# def write_to_json(value: list[dict[str, str]], json_file: str):
#     with open(json_file, 'w') as file:
#         json.dump(value, file, indent=4)

def write_to_json(value: list[dict[str, str]], json_file: str):
    with open(json_file, 'w', encoding='utf-8') as file:
        json.dump(value, file, indent=4, ensure_ascii=False)