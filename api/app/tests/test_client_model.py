import unittest
from .base import BaseTest
from config import Client


class ClientModelTest(BaseTest):
    def tearDown(self):
        self.database.session.query(Client).delete()
        self.database.session.commit()
        return super().tearDown()

    def test_create_success(self):
        all_users = len(Client.query.all())
        Client(
            name='test',
            first_surname='surname',
            second_surname='second',
            birthdate='01-02-1990',
            gender='F',
            email='mail@mail.com',
            phone='550000000',
            postal_code='98000',
            password='secret'
        ).save_to_db()
        self.assertEqual(
            len(Client.query.all()),
            all_users + 1
        )

    def test_required_fields(self):
        all_users = len(Client.query.all())
        try:
            Client(
                first_surname='surname',
                second_surname='second',
                birthdate='01-02-1990',
                gender='F',
                email='mail@mail.com',
                phone='550000000',
                postal_code='98000',
                password='secret'
            ).save_to_db()
            self.assertFalse(True)
        except TypeError as e:
            self.assertIn(
                "missing 1 required positional argument: 'name'",
                str(e)
            )
        try:
            Client(
                name='client name',
                second_surname='second',
                birthdate='01-02-1990',
                gender='F',
                email='mail@mail.com',
                phone='550000000',
                postal_code='98000',
                password='secret'
            ).save_to_db()
            self.assertFalse(True)
        except TypeError as e:
            self.assertIn(
                "missing 1 required positional argument: 'first_surname'",
                str(e)
            )
        try:
            Client(
                name='client name',
                first_surname='surname',
                birthdate='01-02-1990',
                gender='F',
                email='mail@mail.com',
                phone='550000000',
                postal_code='98000',
                password='secret'
            ).save_to_db()
            self.assertFalse(True)
        except TypeError as e:
            self.assertIn(
                "missing 1 required positional argument: 'second_surname'",
                str(e)
            )
        try:
            Client(
                name='client name',
                first_surname='surname',
                second_surname='surname',
                gender='F',
                email='mail@mail.com',
                phone='550000000',
                postal_code='98000',
                password='secret'
            ).save_to_db()
            self.assertFalse(True)
        except TypeError as e:
            self.assertIn(
                "missing 1 required positional argument: 'birthdate'",
                str(e)
            )
        try:
            Client(
                name='client name',
                first_surname='surname',
                second_surname='surname',
                birthdate='01-02-1990',
                email='mail@mail.com',
                phone='550000000',
                postal_code='98000',
                password='secret'
            ).save_to_db()
            self.assertFalse(True)
        except TypeError as e:
            self.assertIn(
                "missing 1 required positional argument: 'gender'",
                str(e)
            )
        try:
            Client(
                name='client name',
                first_surname='surname',
                second_surname='surname',
                birthdate='01-02-1990',
                gender='P',
                phone='550000000',
                postal_code='98000',
                password='secret'
            ).save_to_db()
            self.assertFalse(True)
        except TypeError as e:
            self.assertIn(
                "missing 1 required positional argument: 'email'",
                str(e)
            )
        try:
            Client(
                name='client name',
                first_surname='surname',
                second_surname='surname',
                birthdate='01-02-1990',
                gender='P',
                email='mail@mail.com',
                postal_code='98000',
                password='secret'
            ).save_to_db()
            self.assertFalse(True)
        except TypeError as e:
            self.assertIn(
                "missing 1 required positional argument: 'phone'",
                str(e)
            )
        try:
            Client(
                name='client name',
                first_surname='surname',
                second_surname='surname',
                birthdate='01-02-1990',
                gender='P',
                email='mail@mail.com',
                phone='5523...',
                password='secret'
            ).save_to_db()
            self.assertFalse(True)
        except TypeError as e:
            self.assertIn(
                "missing 1 required positional argument: 'postal_code'",
                str(e)
            )
        try:
            Client(
                name='client name',
                first_surname='surname',
                second_surname='surname',
                birthdate='01-02-1990',
                gender='P',
                email='mail@mail.com',
                phone='5523...',
                postal_code='98653'
            ).save_to_db()
            self.assertFalse(True)
        except TypeError as e:
            self.assertIn(
                "missing 1 required positional argument: 'password'",
                str(e)
            )
        self.assertEqual(
            len(Client.query.all()),
            all_users
        )


if __name__ == '__main__':
    unittest.main()
