from seven_api.resources.JournalResource import JournalResource
from seven_api.resources.SmsResource import SmsResource, StatusMessage
from tests.BaseTest import BaseTest


class TestSms(BaseTest):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resource = SmsResource(self.client)

    def test_status(self) -> None:
        entries = self.resource.status(JournalResource(self.client).outbound()[0]['id'])
        self.assertEqual(1, len(entries))
        entry = entries[0]

        if entry['status'] is None:
            self.assertIsNone(entry['status_time'])
        else:
            self.assertIn(entry['status'], StatusMessage.names())
            self.assertTrue(BaseTest.is_valid_datetime(entry['status_time'], "%Y-%m-%d %H:%M:%S.%f"))

    def test_sms_dispatch__simple(self) -> None:
        to = '491716992343'
        text = 'HEY!!'
        res = self.resource.dispatch(to, text, {'delay': '2050-12-31 12:34:56'})
        self.assertEqual('100', res['success'])
        self.assertIsInstance(res['total_price'], float)
        self.assertIsInstance(res['balance'], float)
        self.assertIsInstance(res['debug'], str)
        self.assertIsInstance(res['sms_type'], str)
        self.assertIsInstance(res['messages'], list)
        self.assertEqual(1, len(res['messages']))

        message = res['messages'][0]
        msg_id = message['id']
        if 'true' == res['debug']:
            self.assertIsNone(msg_id)
        else:
            self.assertIsInstance(msg_id, str)
        self.assertIsInstance(message['sender'], str)
        self.assertEqual(to, message['recipient'])
        self.assertEqual(text, message['text'])
        self.assertEqual('gsm', message['encoding'])
        self.assertEqual(1, message['parts'])
        self.assertIsInstance(message['price'], float)
        self.assertTrue(message['success'])
        self.assertIn('error', message)
        self.assertIsNone(message['error'])
        self.assertIn('error_text', message)
        self.assertIsNone(message['error_text'])

        msg_ids = [msg_id]

        res = self.resource.status(msg_ids)
        self.assertEqual(1, len(res))
        status = res[0]
        self.assertEqual(msg_id, status['id'])
        self.assertIsNone(status['status'])
        self.assertIsNone(status['status_time'])

        res = self.resource.delete(msg_ids)
        self.assertEqual(msg_ids, res['deleted'])
        self.assertTrue(res['success'])
