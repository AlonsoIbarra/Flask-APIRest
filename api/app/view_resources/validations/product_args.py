from flask_restful import reqparse

product_get_args = reqparse.RequestParser()
product_get_args.add_argument(
    'site_client_id',
    required=True,
    help='Site client id field is missing',
    location='args'
)
product_get_args.add_argument(
    'category_id',
    required=True,
    help='Category id field is missing',
    location='args'
)
product_get_args.add_argument(
    'subcategory_ids',
    required=True,
    help='Subcategory list field is missing',
    location='args'
)

list_product_get_args = reqparse.RequestParser()
list_product_get_args.add_argument(
    'site_client_id',
    required=True,
    help='Site client id field is missing',
    location='args'
)
list_product_get_args.add_argument(
    'product_ids',
    required=True,
    help='Product id list field is missing',
    location='args'
)
