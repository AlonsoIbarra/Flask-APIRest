from .base import BaseTest
from config import Product, Category


class ProductModelTest(BaseTest):

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

        return super().setUp()

    def test_required_fields(self):
        all_products = len(Product.query.all())
        try:
            Product(
                short_description='short_description',
                large_description='large_description',
                model='GB43',
                part_number='D23',
                stock=300,
                price=40399.99,
                category=self.category1,
                subcategories=[
                    self.category2
                ],
                url=''
            ).save_to_db()
            self.assertFalse(True)
        except TypeError as e:
            self.assertEqual(
                all_products,
                len(Product.query.all())
            )
            self.assertIn(
                "missing 1 required positional argument: 'name'",
                str(e)
            )

        try:
            Product(
                name='name',
                large_description='large_description',
                model='GB43',
                part_number='D23',
                stock=300,
                price=40399.99,
                category=self.category1,
                subcategories=[
                    self.category2
                ],
                url=''
            ).save_to_db()
            self.assertFalse(True)
        except TypeError as e:
            self.assertEqual(
                all_products,
                len(Product.query.all())
            )
            self.assertIn(
                "missing 1 required positional argument: 'short_description'",
                str(e)
            )

        try:
            Product(
                name='name',
                short_description='short',
                model='GB43',
                part_number='D23',
                stock=300,
                price=40399.99,
                category=self.category1,
                subcategories=[
                    self.category2
                ],
                url=''
            ).save_to_db()
            self.assertFalse(True)
        except TypeError as e:
            self.assertEqual(
                all_products,
                len(Product.query.all())
            )
            self.assertIn(
                "missing 1 required positional argument: 'large_description'",
                str(e)
            )

        try:
            Product(
                name='name',
                short_description='short',
                large_description='Large description',
                part_number='D23',
                stock=300,
                price=40399.99,
                category=self.category1,
                subcategories=[
                    self.category2
                ],
                url=''
            ).save_to_db()
            self.assertFalse(True)
        except TypeError as e:
            self.assertEqual(
                all_products,
                len(Product.query.all())
            )
            self.assertIn(
                "missing 1 required positional argument: 'model'",
                str(e)
            )

        try:
            Product(
                name='name',
                short_description='short',
                large_description='Large description',
                model='G43',
                stock=300,
                price=40399.99,
                category=self.category1,
                subcategories=[
                    self.category2
                ],
                url=''
            ).save_to_db()
            self.assertFalse(True)
        except TypeError as e:
            self.assertEqual(
                all_products,
                len(Product.query.all())
            )
            self.assertIn(
                "missing 1 required positional argument: 'part_number'",
                str(e)
            )

        try:
            Product(
                name='name',
                short_description='short',
                large_description='Large description',
                model='G43',
                part_number='33HJ',
                price=40399.99,
                category=self.category1,
                subcategories=[
                    self.category2
                ],
                url=''
            ).save_to_db()
            self.assertFalse(True)
        except TypeError as e:
            self.assertEqual(
                all_products,
                len(Product.query.all())
            )
            self.assertIn(
                "missing 1 required positional argument: 'stock'",
                str(e)
            )

        try:
            Product(
                name='name',
                short_description='short',
                large_description='Large description',
                model='G43',
                part_number='33HJ',
                stock=300,
                category=self.category1,
                subcategories=[
                    self.category2
                ],
                url=''
            ).save_to_db()
            self.assertFalse(True)
        except TypeError as e:
            self.assertEqual(
                all_products,
                len(Product.query.all())
            )
            self.assertIn(
                "missing 1 required positional argument: 'price'",
                str(e)
            )

        try:
            Product(
                name='name',
                short_description='short',
                large_description='Large description',
                model='G43',
                part_number='33HJ',
                stock=300,
                price=87900.00,
                subcategories=[
                    self.category2
                ],
                url=''
            ).save_to_db()
            self.assertFalse(True)
        except TypeError as e:
            self.assertEqual(
                all_products,
                len(Product.query.all())
            )
            self.assertIn(
                "missing 1 required positional argument: 'category'",
                str(e)
            )

        try:
            Product(
                name='name',
                short_description='short',
                large_description='Large description',
                model='G43',
                part_number='33HJ',
                stock=300,
                price=87900.00,
                category=self.category1,
                url=''
            ).save_to_db()
            self.assertFalse(True)
        except TypeError as e:
            self.assertEqual(
                all_products,
                len(Product.query.all())
            )
            self.assertIn(
                "missing 1 required positional argument: 'subcategories'",
                str(e)
            )

        try:
            Product(
                name='name',
                short_description='short',
                large_description='Large description',
                model='G43',
                part_number='33HJ',
                stock=300,
                price=87900.00,
                category=self.category1,
                subcategories=[]
            ).save_to_db()
            self.assertFalse(True)
        except TypeError as e:
            self.assertEqual(
                all_products,
                len(Product.query.all())
            )
            self.assertIn(
                "missing 1 required positional argument: 'url'",
                str(e)
            )

    def test_required_category_instance(self):
        all_products = len(Product.query.all())
        try:
            Product(
                name='name',
                short_description='short',
                large_description='Large description',
                model='G43',
                part_number='33HJ',
                stock=300,
                price=87900.00,
                category=1,
                subcategories=[],
                url=''
            ).save_to_db()
            self.assertFalse(True)
        except AttributeError:
            self.assertEqual(
                all_products,
                len(Product.query.all())
            )

    def test_create_success(self):
        all_products = len(Product.query.all())
        Product(
            name='test',
            short_description='surname',
            large_description='second',
            model='01-02-1990',
            part_number='F3',
            stock=302,
            price=202.5,
            category=self.category1,
            subcategories=[
                self.category2,
                self.category3
            ],
            url='http://url.com'
        ).save_to_db()
        self.assertEqual(
            len(Product.query.all()),
            all_products + 1
        )
