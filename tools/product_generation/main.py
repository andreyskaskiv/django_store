from tools.product_generation.definitions import (PATH_TO_CATEGORIES_FOR_DB,
                                                  PATH_TO_GOODS_FOR_DB,
                                                  PATH_TO_PARSED_GOODS)
from tools.product_generation.utils import read_json, prepare_categories, write_to_json, categories, prepare_goods


def run():
    products = read_json(PATH_TO_PARSED_GOODS)

    goods_prepare = prepare_goods(products)
    write_to_json(goods_prepare, PATH_TO_GOODS_FOR_DB)

    categories_prepare = prepare_categories(categories)
    write_to_json(categories_prepare, PATH_TO_CATEGORIES_FOR_DB)


if __name__ == '__main__':
    run()
