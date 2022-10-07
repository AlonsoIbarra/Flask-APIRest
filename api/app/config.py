from sqlalchemy.exc import IntegrityError
from utils.jwt_utils import verify_token_middleware
from utils.login_utils import create_signature
from flask import Flask
from flask_restful import Api
from os import getenv
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from utils.login_utils import verify_signature
from utils.jwt_utils import write_token
from flask import request, jsonify
from flask_restful import Resource
from view_resources.validations.login_args import login_post_args
from view_resources.validations.client_args import client_post_args
from view_resources.validations.product_args import product_get_args, \
    list_product_get_args

from functools import wraps
from werkzeug.exceptions import BadRequest


app = Flask(__name__)
api = Api(app)


# DB connection
if getenv('sqlalchemy_database_uri') is not None:
    sqlalchemy_database_uri = getenv('sqlalchemy_database_uri')
else:
    sqlalchemy_database_uri = 'mysql+pymysql://{}:{}@{}/{}'.format(
        getenv('DATABASE_USER'),
        getenv('DATABASE_PASSWORD'),
        getenv('DATABASE_HOST'),
        getenv('DATABASE_NAME')
    )
app.config['SQLALCHEMY_DATABASE_URI'] = sqlalchemy_database_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


marshmallow = Marshmallow(app)


database = SQLAlchemy(app)


class Client(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(100), unique=True, nullable=False)
    first_surname = database.Column(database.String(50), nullable=False)
    second_surname = database.Column(database.String(50), nullable=False)
    birthdate = database.Column(database.String(10), nullable=False)
    gender = database.Column(database.String(1), nullable=False)
    email = database.Column(database.String(120), nullable=False)
    phone = database.Column(database.String(20), nullable=False)
    postal_code = database.Column(database.String(5), nullable=False)
    password = database.Column(database.String(100), nullable=False)

    def __init__(
        self,
        name,
        first_surname,
        second_surname,
        birthdate,
        gender,
        email,
        phone,
        postal_code,
        password
    ):
        self.name = name
        self.first_surname = first_surname
        self.second_surname = second_surname
        self.birthdate = birthdate
        self.gender = gender
        self.email = email
        self.phone = phone
        self.postal_code = postal_code
        self.password = password

    def save_to_db(self):
        database.session.add(self)
        database.session.commit()
        return self


subcategories = database.Table(
    'product_subcategories',
    database.Column(
        'category_id',
        database.Integer,
        database.ForeignKey('category.id'),
        primary_key=True
    ),
    database.Column(
        'product_id',
        database.Integer,
        database.ForeignKey('product.id'),
        primary_key=True
    )
)


class Category(database.Model):
    __tablename__ = "category"
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(40), unique=True, nullable=False)
    products = database.relationship(
        "Product",
        back_populates="category",
        lazy=True,
        cascade="all, delete"
    )

    def __init__(self, name):
        self.name = name

    def save_to_db(self):
        database.session.add(self)
        database.session.commit()
        return self


class Product(database.Model):
    __tablename__ = "product"
    id = database.Column(database.Integer, primary_key=True)
    category_id = database.Column(
        database.Integer,
        database.ForeignKey("category.id")
    )
    category = database.relationship(
        "Category",
        back_populates="products",
        cascade="all, delete"
    )
    subcategories = database.relationship(
        'Category',
        secondary=subcategories,
        lazy='subquery',
        backref=database.backref('category_products', lazy=True)
    )
    name = database.Column(database.String(40), unique=True, nullable=False)
    short_description = database.Column(database.String(300), nullable=False)
    large_description = database.Column(database.String(900), nullable=False)
    model = database.Column(database.String(40), nullable=False)
    part_number = database.Column(database.String(40), nullable=False)
    stock = database.Column(database.Integer, nullable=False)
    price = database.Column(database.Float, nullable=False)
    url = database.Column(database.String(32), nullable=False)

    def __init__(
        self,
        name,
        short_description,
        large_description,
        model,
        part_number,
        stock,
        price,
        category,
        subcategories,
        url
    ):
        self.name = name
        self.short_description = short_description
        self.large_description = large_description
        self.model = model
        self.part_number = part_number
        self.stock = stock
        self.price = price
        self.url = url
        self.category = category
        self.subcategories = subcategories

    def save_to_db(self):
        database.session.add(self)
        database.session.commit()
        return self


class ClientSchema(marshmallow.Schema):
    class Meta:
        model = Client
        load_instance = True


class CategorySchema(marshmallow.SQLAlchemyAutoSchema):
    class Meta:
        model = Category
        load_instance = True


class ProductSchema(marshmallow.SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        include_relationships = True
        load_instance = True


class LoginSchema(marshmallow.Schema):
    class Meta:
        fields = (
            'name',
            'password'
        )


database.create_all()
database.session.commit()


# decorator for verifying the JWT
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        response = verify_token_middleware()
        if response is not None:
            return response
        return f(*args, **kwargs)
    return decorated


class AuthResource(Resource):

    def post(self):
        try:
            data = request.get_json()
        except Exception:
            response = jsonify({
                "success": False,
                "error": "Name and password are required"
            })
            response.status_code = 400
            return response

        try:
            args = login_post_args.parse_args()
        except BadRequest as error:
            args = False
            response = jsonify({
                "success": False,
                "error": str(error.data['message'])
            })
            response.status_code = 400

        if args:
            client = Client.query.filter_by(name=args['name']).first()
            if not client:
                response = jsonify({
                    "success": False,
                    "error": "User not found"
                })
                response.status_code = 400
            else:
                if verify_signature(args['password'], client.password):
                    token = write_token(data=data)
                    response = jsonify({
                        "success": True,
                        "data": str(token),
                    })
                    response.status_code = 200
                else:
                    response = jsonify({
                        "success": False,
                        "error": "Wrong password"
                    })
                    response.status_code = 400

        return response


class ClientResource(Resource):

    @login_required
    def post(self):
        try:
            request.get_json()
        except Exception:
            response = jsonify({
                "success": False,
                "error": "Missing json params"
            })
            response.status_code = 400
            return response

        try:
            args = client_post_args.parse_args()
        except BadRequest as error:
            args = False
            response = jsonify({
                "success": False,
                "error": str(error.data['message'])
            })
            response.status_code = 400

        if args:
            try:
                clientSchema = ClientSchema()
                new_client = Client(
                    name=args['name'],
                    first_surname=args['first_surname'],
                    second_surname=args['second_surname'],
                    birthdate=args['birthdate'],
                    gender=args['gender'],
                    email=args['email'],
                    phone=args['phone'],
                    postal_code=args['postal_code'],
                    password=create_signature(args['password'])
                ).save_to_db()

                write_token(data=clientSchema.dump(new_client))
                response = jsonify({
                    "success": True,
                    "data": {
                        "erp-client-key": new_client.id
                    }
                })
                response.status_code = 201
            except IntegrityError:
                response = jsonify({
                    "success": False,
                    "error": "Client '{}' is already registered"
                    .format(args['name'])
                })
                response.status_code = 400
        return response


class FilterProductsResource(Resource):

    @login_required
    def get(self):
        try:
            request.get_json()
        except Exception:
            response = jsonify({
                "success": False,
                "error": "Missing json params"
            })
            response.status_code = 400
            return response

        try:
            args = product_get_args.parse_args()
        except BadRequest as error:
            args = False
            response = jsonify({
                "success": False,
                "error": str(error.data['message'])
            })
            response.status_code = 400

        if args:
            productSchema = ProductSchema(many=True)

            products = Product.query.filter(
                Product.category.has(id=args['category_id']),
                Product.subcategories.any(
                    Category.id.in_([args['subcategory1_id']])
                ),
                Product.subcategories.any(
                    Category.id.in_([args['subcategory2_id']])
                )
            ).all()
            response = jsonify({
                "success": True,
                "data": productSchema.dump(products)
            })
            response.status_code = 200
        return response


class ListProductsResource(Resource):

    @login_required
    def get(self):
        try:
            request.get_json()
        except Exception:
            response = jsonify({
                "success": False,
                "error": "Missing json params"
            })
            response.status_code = 400
            return response

        try:
            args = list_product_get_args.parse_args()
        except BadRequest as error:
            args = False
            response = jsonify({
                "success": False,
                "error": str(error.data['message'])
            })
            response.status_code = 400

        if args:
            productSchema = ProductSchema(many=True)
            product_id_list = args['product_ids'].split(',')
            products = Product.query.filter(
                Product.id.in_(product_id_list)
            ).all()
            response = jsonify({
                "success": True,
                "data": productSchema.dump(products)
            })
            response.status_code = 200
        return response


# Load resources
api.add_resource(
    ClientResource,
    "/v1/resources/clients"
)
api.add_resource(
    AuthResource,
    "/v1/login"
)

api.add_resource(
    FilterProductsResource,
    "/v1/resources/products/filtered"
)
api.add_resource(
    ListProductsResource,
    "/v1/resources/products/list"
)
