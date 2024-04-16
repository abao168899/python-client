from tests.BaseTest import BaseTest


class TestSevenApi(BaseTest):
    def test_instance(self) -> None:
        self.assertEqual(self.API_KEY, self.client.apiKey)
        self.assertEqual(self.BASE_URL, self.client.baseUrl)
        self.assertEqual(self.SENT_WITH, self.client.sentWith)
