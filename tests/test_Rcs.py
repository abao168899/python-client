from seven_api.resources.RcsResource import RcsTarget, RcsEvent, RcsResource
from tests.BaseTest import BaseTest


class TestRcs(BaseTest):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resource = RcsResource(self.client)

    def test_delete(self) -> None:
        dispatch_res = self.resource.dispatch('+491716992343', 'Hey!', {'delay': '2050-12-31'})
        message = BaseTest.first_list_item_fallback(dispatch_res['messages'])
        res = self.resource.delete(message['id'])
        self.assertEqual(res['success'], True)

    def test_event__is_typing(self) -> None:
        with self.assertRaises(ValueError):
            res = self.resource.event(RcsTarget.PHONE_NUMBER, RcsEvent.IS_TYPING, "491716992343")
            self.assertEqual(res['success'], True)
        self.assertRaises(ValueError)

    def test_event__read(self) -> None:
        with self.assertRaises(ValueError):
            res = self.resource.event(RcsTarget.MESSAGE_ID, RcsEvent.READ, "123")
            self.assertEqual(res['success'], True)

    def test_text(self) -> None:
        res = self.resource.dispatch('+491716992343', 'Hey!', {'delay': '2050-12-31'})
        self.assertEqual(res['success'], '100')
        self.assertIsInstance(res['total_price'], (float, int))
        self.assertIsInstance(res['balance'], float)
        self.assertIsInstance(res['debug'], str)
        self.assertIsInstance(res['sms_type'], str)
        self.assertIsInstance(res['messages'], list)
        self.assertGreater(len(res['messages']), 0)
        message = BaseTest.first_list_item_fallback(res['messages'])
        if message:
            if 'true' == res['debug']:
                self.assertIsNone(message['id'])
            else:
                self.assertIsInstance(message['id'], str)

            self.assertEqual(message['channel'], 'RCS')
            self.assertIsInstance(message['sender'], str)
            self.assertIsInstance(message['recipient'], str)
            self.assertIsInstance(message['text'], str)
            self.assertIsInstance(message['encoding'], str)
            self.assertIsInstance(message['parts'], int)
            self.assertIsInstance(message['price'], (float, int))
            self.assertIsInstance(message['success'], bool)
            self.assertIn('error', message)
            self.assertIn('error_text', message)

            self.resource.delete(message['id'])
