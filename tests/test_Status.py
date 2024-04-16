from seven_api.classes.Status import StatusMessage
from seven_api.resources.JournalResource import JournalResource
from tests.BaseTest import BaseTest


class TestStatus(BaseTest):
    def test_status(self) -> None:
        msg = JournalResource(self.client).outbound()[0]['id']
        res = self.client.status(msg)
        self.assertIsInstance(res, str)

        status, timestamp = res.splitlines()
        self.assertIn(status, StatusMessage.values())
        self.assertTrue(BaseTest.is_valid_datetime(timestamp, "%Y-%m-%d %H:%M:%S.%f"))
