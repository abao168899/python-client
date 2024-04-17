import unittest
import os
import csv
import uuid
from datetime import datetime
from seven_api.SevenApi import SevenApi


class BaseTest(unittest.TestCase):
    API_KEY = os.environ.get('SEVEN_API_KEY')
    BASE_URL = 'https://gateway.seven.io/api'
    SENT_WITH = 'Python-Test'

    @staticmethod
    def is_valid_datetime(timestamp: str, formatting: str) -> bool:
        try:
            datetime.strptime(timestamp, formatting)
            return True
        except ValueError:
            return False

    @staticmethod
    def create_random_url() -> str:
        return "http://python.tld/{0}".format(str(uuid.uuid4()))

    def __init__(self, *args, **kwargs) -> None:
        super(BaseTest, self).__init__(*args, **kwargs)

        self.client = SevenApi(self.API_KEY, self.SENT_WITH, self.BASE_URL)


if __name__ == '__main__':
    unittest.main()
