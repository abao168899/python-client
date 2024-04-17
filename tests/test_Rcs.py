from seven_api.resources.RcsResource import RcsTarget, RcsEvent, RcsResource
from tests.BaseTest import BaseTest


class TestRcs(BaseTest):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resource = RcsResource(self.client)

    def test_delete(self) -> None:
        message = self.resource.dispatch('+491716992343', 'Hey!', {'delay': '2050-12-31'}).messages[0]
        res = self.resource.delete(message.id)
        self.assertTrue(res.success)

    def test_event__is_typing(self) -> None:
        with self.assertRaises(ValueError):
            res = self.resource.event(RcsTarget.PHONE_NUMBER, RcsEvent.IS_TYPING, "491716992343")
            self.assertTrue(res.success)
        self.assertRaises(ValueError)

    def test_event__read(self) -> None:
        with self.assertRaises(ValueError):
            res = self.resource.event(RcsTarget.MESSAGE_ID, RcsEvent.READ, "123")
            self.assertTrue(res.success)

    def test_text(self) -> None:
        to = '491716992343'
        text = 'Hey!'
        res = self.resource.dispatch(to, text, {'delay': '2050-12-31'})
        self.assertEqual('100', res.success)
        self.assertGreaterEqual(res.total_price, 0.0)
        self.assertIn(res.debug, ['true', 'false'])
        self.assertEqual('direct', res.sms_type)
        self.assertEqual(1, len(res.messages))
        message = res.messages[0]
        if 'true' == res.debug:
            self.assertIsNone(message.id)
        else:
            self.assertIsInstance(message.id, str)

        self.assertEqual('RCS', message.channel)
        self.assertTrue(len(message.sender) > 0)
        self.assertEqual(to, message.recipient)
        self.assertEqual(text, message.text)
        self.assertIsInstance(message.encoding, str)
        self.assertIsNone(message.error)
        self.assertIsNone(message.error_text)
        self.assertEqual(1, message.parts)
        self.assertGreaterEqual(message.price, 0.0)
        self.assertTrue(message.success)

        self.resource.delete(message.id)
