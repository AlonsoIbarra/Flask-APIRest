from .utils.utils import postal_code_validation,\
    birthdate_validation, email_validation, phone_validation
from flask_restful import reqparse

client_post_args = reqparse.RequestParser()

client_post_args.add_argument(
    'site_client_id',
    required=True,
    help='Site client id field is required'
)
client_post_args.add_argument(
    'name',
    required=True,
    help='Name field is required'
)
client_post_args.add_argument(
    'first_surname',
    required=True,
    help='First surname field is required'
)
client_post_args.add_argument(
    'second_surname',
    required=True,
    help='Second surname field is required'
)
client_post_args.add_argument(
    'birthdate',
    required=True,
    type=birthdate_validation()
)
client_post_args.add_argument(
    'gender',
    choices=('M', 'F'),
    required=True,
    help='Bad choice: {error_msg}'
)
client_post_args.add_argument(
    'email',
    required=True,
    type=email_validation()
)
client_post_args.add_argument(
    'phone',
    required=True,
    type=phone_validation(20)
)
client_post_args.add_argument(
    'postal_code',
    type=postal_code_validation(5),
    required=True
)
client_post_args.add_argument(
    'password',
    required=True,
    help='Password field is required'
)
