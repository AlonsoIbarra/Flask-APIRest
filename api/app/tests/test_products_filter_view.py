import json

from config import Category, Product
from .base import BaseTest


class ProductsFilterViewTest(BaseTest):

    def __init__(self, methodName: str = ...):
        super().__init__(methodName)
        self.url = '/v1/resources/products/filtered'

    def setUp(self):
        # Remove older references
        for prod in Product.query.all():
            prod.subcategories = []
            prod.save_to_db()
            prod.query.delete()
        for cat in Category.query.all():
            cat.query.delete()
        self.database.session.commit()

        self.category1 = Category(
                name='category 1'
            ).save_to_db()

        self.category2 = Category(
                name='category 2'
            ).save_to_db()

        self.category3 = Category(
                name='category 3'
            ).save_to_db()

        Product(
            name='Product 1',
            short_description='short_description',
            large_description='large_description',
            model='GB43',
            part_number='D23',
            stock=300,
            price=40399.99,
            category=self.category1,
            subcategories=[
                self.category2,
                self.category3,
            ],
            url=''
        ).save_to_db()

        return super().setUp()

    def test_auth_required(self):
        tester = self.app.test_client(self)
        response = tester.get(
            self.url,
            headers={'Content-Type': 'application/json'}
        )
        self.assertEqual(response.status_code, 401)
        self.assertIn('Authentication needed', str(response.data))

    def test_invalid_token(self):
        tester = self.app.test_client(self)
        response = tester.get(
            self.url,
            headers={
                'Content-Type': 'application/json',
                'Authorization': u'Bearer fake_token_123'
            }
        )
        self.assertEqual(response.status_code, 401)
        self.assertIn('Invalid Token', str(response.data))

    def test_missing_params(self):
        tester = self.app.test_client(self)
        response = tester.get(
            self.url,
            headers=self.headers
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('Missing json params', str(response.data))

        response = tester.get(
            self.url,
            headers=self.headers,
            data=json.dumps(
                {
                    'category_id': '2'
                }
            )
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('site_client_id', str(response.data))

        response = tester.get(
            self.url,
            headers=self.headers,
            data=json.dumps(
                {
                    'site_client_id': '',
                    'category_id': '2'
                }
            )
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('subcategory1_id', str(response.data))

        response = tester.get(
            self.url,
            headers=self.headers,
            data=json.dumps(
                {
                    'site_client_id': '',
                    'category_id': '2',
                    'subcategory1_id': '2'
                }
            )
        )
        self.assertEqual(response.status_code, 400)

    def test_empty_data_request(self):
        tester = self.app.test_client(self)
        response = tester.get(
            self.url,
            headers=self.headers,
            data=json.dumps(
                {
                    'site_client_id': '',
                    'category_id': '-1',
                    'subcategory1_id': '-1',
                    'subcategory2_id': '-1'
                }
            )
        )

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertEqual(len(data['data']), 0)

    def test_not_empty_data_request(self):
        tester = self.app.test_client(self)
        response = tester.get(
            self.url,
            headers=self.headers,
            data=json.dumps(
                {
                    'site_client_id': '',
                    'category_id': self.category1.id,
                    'subcategory1_id': self.category2.id,
                    'subcategory2_id': self.category3.id
                }
            )
        )

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertEqual(len(data['data']), 1)
        self.assertIn('Product 1', str(data['data']))