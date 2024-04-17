from seven_api.SevenApi import SevenApi


class Resource:
    __api: SevenApi

    def __init__(self, client: SevenApi):
        self.__api = client
