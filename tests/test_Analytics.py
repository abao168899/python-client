from datetime import datetime, timedelta

from seven_api.resources.AnalyticsResource import AnalyticsResource, AnalyticsParams
from tests.BaseTest import BaseTest


class TestAnalytics(BaseTest):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resource = AnalyticsResource(self.client)

    def test_analytics_by_label(self) -> None:
        res = self.resource.by_label(AnalyticsParams())

        for entry in res:
            self.assertIsInstance(entry['label'], str)
            self.assert_base(entry)

    def test_analytics_by_subaccount(self) -> None:
        res = self.resource.by_subaccount(AnalyticsParams())

        for entry in res:
            self.assertIsInstance(entry['account'], str)
            self.assert_base(entry)

    def test_analytics_by_date(self) -> None:
        res = self.resource.by_date(AnalyticsParams())

        for entry in res:
            self.assertIsInstance(entry['date'], str)
            self.assert_base(entry)

    def test_analytics_by_country(self) -> None:
        today = datetime.today()
        params = AnalyticsParams()
        params.end = today.strftime('%Y-%m-%d')
        params.label = 'label'
        params.start = (today - timedelta(days=90)).strftime('%Y-%m-%d')
        res = self.resource.by_country(params)

        self.assertIsInstance(res, list)

        msg = BaseTest.first_list_item_fallback(res)
        if msg:
            self.assertIsInstance(msg['country'], str)
            self.assert_base(msg)

    def assert_base(self, msg: dict):
        self.assertIsInstance(msg['hlr'], int)
        self.assertIsInstance(msg['inbound'], int)
        self.assertIsInstance(msg['mnp'], int)
        self.assertIsInstance(msg['sms'], int)
        self.assertTrue(isinstance(msg['usage_eur'], int) or isinstance(msg['usage_eur'], float))
        self.assertIsInstance(msg['voice'], int)
