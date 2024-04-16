from seven_api.resources.RcsResource import RcsTarget, RcsEvent, RcsResource
from tests.BaseTest import BaseTest


class TestRcs(BaseTest):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resource = RcsResource(self.client)

    def test_delete(self) -> None:
        message = self.resource.dispatch('+491716992343', 'Hey!', {'delay': '2050-12-31'})['messages'][0]
        res = self.resource.delete(message['id'])
        self.assertTrue(res['success'])

    def test_event__is_typing(self) -> None:
        with self.assertRaises(ValueError):
            res = self.resource.event(RcsTarget.PHONE_NUMBER, RcsEvent.IS_TYPING, "491716992343")
            self.assertTrue(res['success'])
        self.assertRaises(ValueError)

    def test_event__read(self) -> None:
        with self.assertRaises(ValueError):
            res = self.resource.event(RcsTarget.MESSAGE_ID, RcsEvent.READ, "123")
            self.assertTrue(res['success'])

    def test_text(self) -> None:
        to = '491716992343'
        text = 'Hey!'
        res = self.resource.dispatch(to, text, {'delay': '2050-12-31'})
        self.assertEqual('100', res['success'])
        self.assertIsInstance(res['total_price'], (float, int))
        self.assertIsInstance(res['balance'], float)
        self.assertIsInstance(res['debug'], str)
        self.assertIsInstance(res['sms_type'], str)
        self.assertIsInstance(res['messages'], list)
        self.assertEqual(1, len(res['messages']))
        message = res['messages'][0]
        if 'true' == res['debug']:
            self.assertIsNone(message['id'])
        else:
            self.assertIsInstance(message['id'], str)

        self.assertEqual('RCS', message['channel'])
        self.assertIsInstance(message['sender'], str)
        self.assertEqual(to, message['recipient'])
        self.assertEqual(text, message['text'])
        self.assertIsInstance(message['encoding'], str)
        self.assertIn('error', message)
        self.assertIn('error_text', message)
        self.assertIsInstance(message['parts'], int)
        self.assertIsInstance(message['price'], (float, int))
        self.assertIsInstance(message['success'], bool)

        self.resource.delete(message['id'])
