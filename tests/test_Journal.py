from seven_api.resources.JournalResource import JournalResource, JournalParams
from tests.BaseTest import BaseTest


class TestJournal(BaseTest):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resource = JournalResource(self.client)

    def test_inbound(self) -> None:
        for entry in self.resource.inbound():
            self.__assert_common(entry)

    def test_outbound(self) -> None:
        params = JournalParams()
        params.limit = 500
        params.date_from = ""
        params.date_to = ""
        params.state = ""
        params.to = ""

        for entry in self.resource.outbound(params):
            self.__assert_common(entry)

            self.assertIn('channel', entry)

            self.assertIsInstance(entry['connection'], str)
            self.assertGreater(len(entry['connection']), 0)

            self.assertIn('dlr', entry)
            if entry['dlr'] is not None:
                self.assertIsInstance(entry['dlr'], str)
                self.assertGreater(len(entry['dlr']), 0)

            self.assertIn('dlr_timestamp', entry)
            if entry['dlr_timestamp'] is not None:
                self.assertIsInstance(entry['dlr_timestamp'], str)
                self.assertGreater(len(entry['dlr_timestamp']), 0)

            self.assertIn('foreign_id', entry)
            if entry['foreign_id'] is not None:
                self.assertIsInstance(entry['foreign_id'], str)
                self.assertGreater(len(entry['foreign_id']), 0)

            self.assertIn('label', entry)
            if entry['label'] is not None:
                self.assertIsInstance(entry['label'], str)
                self.assertGreater(len(entry['label']), 0)

            self.assertIn('latency', entry)
            if entry['latency'] is not None:
                self.assertIsInstance(entry['latency'], str)
                self.assertGreater(len(entry['latency']), 0)

            self.assertIn('mccmnc', entry)
            if entry['mccmnc'] is not None:
                self.assertIsInstance(entry['mccmnc'], str)
                self.assertGreater(len(entry['mccmnc']), 0)

            self.assertIsInstance(entry['type'], str)
            self.assertGreater(len(entry['type']), 0)

    def test_replies(self) -> None:
        for entry in self.resource.replies():
            self.__assert_common(entry)

    def test_voice(self) -> None:
        for entry in self.resource.voice():
            self.__assert_common(entry)

            duration = entry['duration']
            if duration is not None:
                self.assertGreater(len(duration), 0)
            self.assertTrue(type(duration) is str or duration is None)

            error = entry['error']
            self.assertTrue(error is None or type(error) is str)

            self.assertIsInstance(entry['id'], str)
            self.assertIsInstance(entry['from'], str)

            price = entry['price']
            self.assertTrue(price is None or type(price) is str)

            self.assertIsInstance(entry['status'], str)
            self.assertIsInstance(entry['text'], str)
            self.assertIsInstance(entry['timestamp'], str)
            self.assertIsInstance(entry['to'], str)
            self.assertIsInstance(entry['xml'], bool)

    def __assert_common(self, entry: dict):
        self.assertIsInstance(entry['from'], str)
        self.assertLessEqual(len(entry['from']), 16)

        self.assertIsInstance(entry['id'], str)
        self.assertGreater(len(entry['id']), 0)

        self.assertIn('price', entry)
        price_type = type(entry['price'])
        if price_type is str:
            self.assertGreater(len(entry['price']), 0)
        elif price_type is int:
            self.assertGreaterEqual(entry['price'], 0)
        # self.assertIsInstance(entry['price'], str)
        # self.assertGreater(len(entry['price']), 0)

        self.assertIsInstance(entry['text'], str)

        self.assertIsInstance(entry['timestamp'], str)
        self.assertGreater(len(entry['timestamp']), 0)

        self.assertIsInstance(entry['to'], str)
        self.assertGreater(len(entry['to']), 0)
