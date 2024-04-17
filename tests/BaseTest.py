import unittest
import os
import uuid
from datetime import datetime
from seven_api.SevenApi import SevenApi
import logging

logging.basicConfig(
    format="%(levelname)s [%(asctime)s] %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO
)

class BaseTest(unittest.TestCase):
    API_KEY = os.environ.get('SEVEN_API_KEY')
    BASE_URL = 'https://gateway.seven.io/api'
    SENT_WITH = 'Python-Test'
    SIGNING_SECRET = os.environ.get('SEVEN_SIGNING_SECRET')

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

        self.client = SevenApi(self.API_KEY, self.SIGNING_SECRET, self.SENT_WITH, self.BASE_URL)


if __name__ == '__main__':
    unittest.main()
