import os
from pathlib import Path
from store.settings import BASE_DIR


PATH_TO_PRODUCT_GENERATION = os.path.dirname(__file__)

PATH_TO_GOODS_FOR_DB = os.path.join(PATH_TO_PRODUCT_GENERATION, 'goods_for_db.json')
PATH_TO_CATEGORIES_FOR_DB = os.path.join(PATH_TO_PRODUCT_GENERATION, 'categories_for_db.json')

PATH_TO_PARSED_GOODS = os.path.join(PATH_TO_PRODUCT_GENERATION, 'parsed_goods.json')













