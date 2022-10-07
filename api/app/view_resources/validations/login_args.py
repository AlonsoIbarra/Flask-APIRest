from flask_restful import reqparse

login_post_args = reqparse.RequestParser()
login_post_args.add_argument(
    'name',
    required=True,
    help='Name field is required'
)
login_post_args.add_argument(
    'password',
    required=True,
    help='Password field is required'
)
