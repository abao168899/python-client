import time

from seven_api.resources.SubaccountsResource import SubaccountsResource, Subaccount
from tests.BaseTest import BaseTest


class TestSubaccounts(BaseTest):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resource = SubaccountsResource(self.client)

    def test_subaccounts_create_fail(self) -> None:
        res = self.resource.create('', '')

        self.assertIsInstance(res.error, str)
        self.assertIsNone(res.subaccount)
        self.assertFalse(res.success)

    def test_subaccounts_create_success(self) -> None:
        timestamp = int(time.time())
        email = f'tom.test.{timestamp}@seven.io'
        name = f'Tom Test {timestamp}'
        res = self.resource.create(email, name)

        self.assertEqual(email, res.subaccount.contact.email)
        self.assertEqual(name, res.subaccount.contact.name)

        self.assertIsNone(res.error)
        self.__assertSubaccount(res.subaccount)
        self.assertTrue(res.success)

        self.resource.delete(res.subaccount.id)

    def test_subaccounts_delete_fail(self) -> None:
        res = self.resource.delete(123456)
        self.assertEqual('Subaccount not found', res.error)
        self.assertFalse(res.success)

    def test_subaccounts_list(self) -> None:
        timestamp = int(time.time())
        sub_id = self.resource.create(f'tom.test.{timestamp}@seven.io', f'Tom Test {timestamp}').subaccount.id
        res = self.resource.list(sub_id)
        self.assertTrue(len(res) == 1)

        self.__assertSubaccount(res[0])

        self.resource.delete(sub_id)

    def test_subaccounts_list_with_id__empty(self) -> None:
        res = self.resource.list(0)
        self.assertEqual(len(res), 0)

    def test_subaccounts_transfer_credits_fail(self) -> None:
        res = self.resource.transfer_credits(0, 0.0)
        self.assertEqual('Invalid amount', res.error)
        self.assertFalse(res.success)

    def test_subaccounts_update_fail(self) -> None:
        res = self.resource.auto_charge(0, 0.0, 0.0)
        self.assertEqual('Subaccount not found', res.error)
        self.assertFalse(res.success)

    def __assertSubaccount(self, subaccount: Subaccount):
        if subaccount.auto_topup.amount is not None:
            self.assertGreaterEqual(subaccount.auto_topup.amount, 0.0)
        if subaccount.auto_topup.threshold is not None:
            self.assertGreaterEqual(subaccount.auto_topup.threshold, 0.0)

        self.assertGreater(len(subaccount.contact.email), 0)
        self.assertGreater(len(subaccount.contact.name), 0)
        self.assertGreater(subaccount.id, 0)
        self.assertGreaterEqual(subaccount.total_usage, 0.0)
