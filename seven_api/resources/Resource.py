from seven_api.SevenApi import SevenApi


class Resource:
    def __init__(self, client: SevenApi):
        self._api = client
