from seven_api.resources.VoiceResource import VoiceResource
from tests.BaseTest import BaseTest


class TestVoice(BaseTest):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resource = VoiceResource(self.client)

    def test_validate_phone_number__fail(self):
        phone = '0'
        res = self.resource.validate_phone_number(phone)
        self.assertEqual('Shortcodes are not allowed.', res.error)
        self.assertEqual(phone, res.formatted_output)
        self.assertIsNone(res.id)
        self.assertEqual(phone, res.sender)
        self.assertFalse(res.success)
        self.assertFalse(res.voice)

    def test_dispatch_text(self) -> None:
        to = '491716992343'
        text = 'Hello there!'
        res = self.resource.dispatch(to, text, {'from': None, 'ringtime': None})

        # self.assertEqual('100', res.success)
        self.assertTrue(len(res.success) == 3)
        self.assertIsInstance(res.total_price, float)
        self.assertIsInstance(res.balance, float)
        self.assertIsInstance(res.debug, bool)
        self.assertIsInstance(res.messages, list)
        self.assertEqual(1, len(res.messages))

        message = res.messages[0]
        msg_id = message.id
        if res.debug:
            self.assertIsNone(msg_id)
        else:
            self.assertIsInstance(msg_id, int)
        self.assertIsInstance(message.sender, str)
        self.assertEqual(to, message.recipient)
        self.assertEqual(text, message.text)
        self.assertIsInstance(message.price, float)
        # self.assertTrue(message.success)
        self.assertIsNone(message.error)
        self.assertIsNone(message.error_text)
