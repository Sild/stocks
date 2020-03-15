import os


class Config:
    @staticmethod
    def __get_token():
        token = ""
        try:
            token = os.environ['TINKOFF_API_TOKEN']
        except Exception as e:
            pass
        if len(token) == 0:
            token = input("Enter token: ")
        return token

    def __init__(self):
        self.api_token = self.__get_token()
