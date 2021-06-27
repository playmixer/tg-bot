import requests


class TelegramBot:
    app = None
    api_url = None
    token = None
    update_id = 0
    handlers = {}
    data = None

    def init_base(self, base):
        self.data = base

    def __init__(self, token):
        self.singleton(self)
        self.token = token
        self.api_url = 'https://api.telegram.org/bot' + token + '/'

    @classmethod
    def _request(cls, url, params=None):
        return requests.post(url, json=params)

    @classmethod
    def singleton(cls, app):
        cls.app = app

    """
    Bot API Methods
    """

    def _method(self, method, params=None):
        url = self.api_url + method
        return self._request(url, params)

    def get_updates(self):
        update_id = self.data.get_update_id() + 1
        return self._method(f'getUpdates?offset={update_id}')

    def send_message(self, chat_id: int, text: str, reply_markup: dict = None):
        params = dict()
        params['chat_id'] = chat_id
        params['text'] = text
        if reply_markup:
            params['reply_markup'] = reply_markup
        return self._method(f'sendMessage', params=params)

    """
    END Bot API Methods
    """
