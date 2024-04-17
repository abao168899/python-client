from seven_api.SevenApi import SevenApi
from seven_api.resources.BalanceResource import BalanceResource

client = SevenApi("InsertYourSuperSecretApiKeyFromSeven")
resource = BalanceResource(client)
balance = resource.retrieve()
amount = balance['amount']
currency = balance['currency']

print(f'Balance: {amount} {currency}')
