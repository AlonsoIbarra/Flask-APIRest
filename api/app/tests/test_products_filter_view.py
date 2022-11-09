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

        url = self.url + '?category_id=2'
        response = tester.get(
            url,
            headers=self.headers
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('site_client_id', str(response.data))

        url = self.url + '?site_client_id=&category_id=2'
        response = tester.get(
            url,
            headers=self.headers
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('subcategory_ids', str(response.data))

        url = self.url + '?site_client_id=2&subcategory_ids=2'
        response = tester.get(
            url,
            headers=self.headers
        )
        self.assertEqual(response.status_code, 400)

    def test_empty_data_request(self):
        tester = self.app.test_client(self)

        url = self.url + '?site_client_id=&category_id=-1&subcategory_ids=-1'
        response = tester.get(
            url,
            headers=self.headers
        )

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertEqual(len(data['data']), 0)

    def test_not_empty_data_request(self):
        tester = self.app.test_client(self)

        url = self.url + '?site_client_id=&category_id={}&'\
            'subcategory_ids={}'\
            .format(
                self.category1.id,
                self.category2.id
            )
        response = tester.get(
            url,
            headers=self.headers
        )

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertEqual(len(data['data']), 1)
        self.assertIn('Product 1', str(data['data']))
