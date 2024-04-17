from seven_api.resources.JournalResource import JournalResource, JournalParams, JournalBase
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

            self.assertGreater(len(entry.connection), 0)

            if entry.dlr is not None:
                self.assertGreater(len(entry.dlr), 0)

            if entry.dlr_timestamp is not None:
                self.assertGreater(len(entry.dlr_timestamp), 0)

            if entry.foreign_id is not None:
                self.assertGreater(len(entry.foreign_id), 0)

            if entry.label is not None:
                self.assertGreater(len(entry.label), 0)

            if entry.latency is not None:
                self.assertGreater(len(entry.latency), 0)

            if entry.mccmnc is not None:
                self.assertGreater(len(entry.mccmnc), 0)

            self.assertGreater(len(entry.type), 0)

    def test_replies(self) -> None:
        for entry in self.resource.replies():
            self.assertGreaterEqual(entry.price, 0.0)
            self.__assert_common(entry, False)

    def test_voice(self) -> None:
        for entry in self.resource.voice():
            self.__assert_common(entry)

            if entry.duration is not None:
                self.assertGreater(len(entry.duration), 0)

            self.assertTrue(len(entry.id) > 0)
            self.assertTrue(len(entry.from_) > 0)

            if entry.price is not None:
                self.assertTrue(len(entry.price) > 0)

            self.assertTrue(len(entry.text) > 0)
            self.assertTrue(len(entry.timestamp) > 0)
            self.assertTrue(len(entry.to) > 0)

    def __assert_common(self, entry: JournalBase, assert_price = True):
        self.assertLessEqual(len(entry.from_), 16)

        self.assertGreater(len(entry.id), 0)

        if assert_price:
            self.assertFalse(entry.price == "0.0")

        self.assertLessEqual(len(entry.text), 10000)
        self.assertGreater(len(entry.timestamp), 0)
        self.assertGreater(len(entry.to), 0)
