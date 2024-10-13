<img src="https://www.seven.io/wp-content/uploads/Logo.svg" width="250" />


# Python API Client

## Installation

Make sure you have [Python 3](https://www.python.org/downloads/) installed.

```shell script
pip3 install sms77api
```

### Methods

```python
def __init__(self, api_key: str, sent_with: str = 'Python'):
    pass


def analytics(self, params={SMS001}):
    pass


def balance(self, api_key: str = None):
    pass


def contacts(self, action: ContactsAction, params: dict = {SMS001}):
    pass


def hooks(self, action: HooksAction, params: dict = {SMS001}):
    pass


def journal(self, typ: JournalType, params: dict = {SMS001}):
    pass


def lookup(self, typ: LookupType, number: str, json: bool = False):
    pass


def pricing(self, format_: PricingFormat = PricingFormat.CSV, country: str = None):
    pass


def sms(self, to: str, text: str, params: dict = {SMS001}):
    pass


def status(self, msg_id: int):
    pass


def subaccounts(self, action: SubaccountsAction, params: dict = {SMS001}):
    pass


def validate_for_voice(self, number: str, callback: str = None):
    pass


def voice(self, to: str, text: str, params: dict = {SMS001}):
    pass
```

### Examples

#### Retrieve balance associated with given API key

```python
from sms77api.Sms77api import Sms77api

client = Sms77api("SMS001")
print(client.balance())
```

#### Send an SMS and return a detailed JSON response

```python
from sms77api.Sms77api import Sms77api
import os

client = Sms77api(os.environ.get('SMS77_API_KEY', 'd16fA5fa8d1bb3C79F1e2e615f5c0c566137f050b5C490F365773265caf4266E'))
print(client.sms('+491771783130', 'Hi friend!', {'json': True}))
```

#### Support

Need help? Feel free to [contact us](https://www.sms77.io/en/company/contact/).

###### License

[![MIT](https://img.shields.io/badge/License-MIT-teal.svg)](LICENSE)
