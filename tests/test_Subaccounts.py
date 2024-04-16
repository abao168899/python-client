import time

from seven_api.resources.SubaccountsResource import SubaccountsResource
from tests.BaseTest import BaseTest


class TestSubaccounts(BaseTest):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resource = SubaccountsResource(self.client)

    def test_subaccounts_create_fail(self) -> None:
        res = self.resource.create('', '')

        self.assertIsInstance(res['error'], str)
        self.assertNotIn('subaccount', res)
        self.assertFalse(res['success'])

    def test_subaccounts_create_success(self) -> None:
        timestamp = int(time.time())
        email = f'tom.test.{timestamp}@seven.io'
        name = f'Tom Test {timestamp}'
        res = self.resource.create(email, name)

        self.assertIn('error', res)
        self.assertIsNone(res['error'])
        self.__assertSubaccount(res['subaccount'])
        self.assertTrue(res['success'])

        self.resource.delete(res['subaccount']['id'])

    def test_subaccounts_delete_fail(self) -> None:
        res = self.resource.delete(123456)
        self.assertFalse(res['success'])
        self.assertEqual('Subaccount not found', res['error'])

    def test_subaccounts_list(self) -> None:
        timestamp = int(time.time())
        email = f'tom.test.{timestamp}@seven.io'
        name = f'Tom Test {timestamp}'
        created = self.resource.create(email, name)

        for subaccount in self.resource.list():
            self.__assertSubaccount(subaccount)

        self.resource.delete(created['subaccount']['id'])

    def test_subaccounts_list_with_id__empty(self) -> None:
        res = self.resource.list(0)
        self.assertEqual(len(res), 0)

    def test_subaccounts_transfer_credits_fail(self) -> None:
        res = self.resource.transfer_credits(0, 0.0)
        self.assertFalse(res['success'])
        self.assertEqual('Invalid amount', res['error'])

    def test_subaccounts_update_fail(self) -> None:
        res = self.resource.auto_charge(0, 0.0, 0.0)
        self.assertFalse(res['success'])
        self.assertEqual('Subaccount not found', res['error'])

    def __assertSubaccount(self, subaccount):
        auto_topup = subaccount['auto_topup']

        self.assertIn('amount', auto_topup)
        self.assertTrue(isinstance(auto_topup['amount'], (float, type(None))))

        self.assertIn('threshold', auto_topup)
        self.assertTrue(isinstance(auto_topup['threshold'], (float, int, type(None))))

        self.assertIn('balance', subaccount)
        self.assertTrue(isinstance(subaccount['balance'], (float, int)))

        self.assertIn('company', subaccount)
        self.assertIsInstance(subaccount['company'], str)

        contact = subaccount['contact']
        self.assertIsInstance(contact['email'], str)
        self.assertIsInstance(contact['name'], str)

        self.assertIn('id', subaccount)
        self.assertIsInstance(subaccount['id'], int)

        self.assertIn('total_usage', subaccount)
        self.assertIsInstance(subaccount['total_usage'], int)

        self.assertIn('username', subaccount)
        self.assertTrue(isinstance(subaccount['username'], (str, type(None))))
