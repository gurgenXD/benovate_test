from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from users.forms import SendMoneyForm


User = get_user_model()


class UserModelTest(TestCase):
    def setUp(self):
        User.objects.create(
            username='user_for_test',
            inn='36640693971',
            money=1000.00
        )
        User.objects.create(
            username='user_for_test2',
            inn='36640692271',
            money=200.00
        )

    def test_inn_unique(self):
        with self.assertRaises(IntegrityError):
            User.objects.create(
                username='user_for_test1',
                inn='36640693971',
                money=1000.00
            )

    def test_inn_validator(self):
        user = User.objects.create(
            username='user_for_test1',
            inn='test_text',
            money=1000.00
        )

        with self.assertRaises(ValidationError):
            user.full_clean()

    def test_money_validator(self):
        user = User.objects.create(
            username='user_for_test1',
            inn='36640693972',
            money=-1000.00
        )

        with self.assertRaises(ValidationError):
            user.full_clean()

    def test_send_money_form(self):
        test_data_with_errors = [
            {'from_user': '1', 'money': '-1000', 'to_users': '36640692271'},
            {'from_user': '31', 'money': '1000', 'to_users': '36640692271'},
            {'from_user': '1', 'money': '1000', 'to_users': '36640693971'},
        ]

        test_data = [
            {'from_user': '1', 'money': '1000', 'to_users': '36640692271'},
        ]

        for data in test_data_with_errors:
            form = SendMoneyForm(data=data)
            self.assertNotEqual(form.is_valid(), True)

        for data in test_data:
            form = SendMoneyForm(data=data)
            self.assertEqual(form.is_valid(), True)

    def test_send_money_view(self):
        test_data_with_errors = [
            {'from_user': '1', 'money': '-1000', 'to_users': '36640692271'},
            {'from_user': '31', 'money': '1000', 'to_users': '36640692271'},
            {'from_user': '1', 'money': '1000', 'to_users': '36640693971'},
        ]

        test_data = [
            {'from_user': '1', 'money': '1000', 'to_users': '36640692271'},
        ]

        response_get = self.client.get('/users/send-money/3')
        self.assertNotEqual(response_get.status_code, 200)

        for data in test_data_with_errors:
            response_post = self.client.post('/users/send-money', data=data)
            self.assertNotEqual(response_post.status_code, 302)

        for data in test_data:
            response_get = self.client.get('/users/send-money')
            self.assertEqual(response_get.status_code, 200)

            response_post = self.client.post('/users/send-money', data=data)
            self.assertEqual(response_post.status_code, 302)
