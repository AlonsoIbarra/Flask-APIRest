import json
from config import Category, Product
from .base import BaseTest


class ProductsListViewTest(BaseTest):

    def __init__(self, methodName: str = ...):
        super().__init__(methodName)
        self.url = '/v1/resources/products/list'

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

        self.product = Product(
            name='Product 1',
            short_description='short_description',
            large_description='large_description',
            model='GB43',
            part_number='D23',
            stock=300,
            price=40399.99,
            category=self.category1,
            subcategories=[],
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

        url = self.url + '?site_client_id=2'
        response = tester.get(
            url,
            headers=self.headers
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            'Product id list field is missing',
            str(response.data)
        )

        url = self.url + '?product_ids=2'
        response = tester.get(
            url,
            headers=self.headers
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            'Site client id field is missing',
            str(response.data)
        )

    def test_empty_response_data(self):
        tester = self.app.test_client(self)

        url = self.url + '?product_ids=0&site_client_id=2'
        response = tester.get(
            url,
            headers=self.headers
        )

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertEqual(len(data['data']), 0)

    def test_not_empty_response_data(self):
        tester = self.app.test_client(self)

        url = self.url + '?product_ids={}&site_client_id=2'\
            .format(str(self.product.id))
        response = tester.get(
            url,
            headers=self.headers
        )

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertEqual(len(data['data']), 1)
        self.assertIn('Product 1', str(data['data']))

