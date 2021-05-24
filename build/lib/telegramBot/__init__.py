import requests
from time import sleep
from pydantic import BaseModel, Field
from typing import List, Optional
from abc import abstractmethod, ABC


class TGetUpdateResultMessageChat(BaseModel):
    id: int
    first_name: str
    last_name: Optional[str]
    username: str
    type: str


class TGetUpdateResultMessageFrom(BaseModel):
    id: int
    is_bot: bool
    first_name: str
    last_name: Optional[str]
    username: str
    language_code: Optional[str]


class TGetUpdatesResultMessage(BaseModel):
    message_id: int
    from_: TGetUpdateResultMessageFrom = Field(alias='from')
    chat: TGetUpdateResultMessageChat
    date: int
    text: str


class TGetUpdatesResultCallBackQuery(BaseModel):
    id: int
    from_: TGetUpdateResultMessageFrom = Field(alias='from')
    message: TGetUpdatesResultMessage
    date: Optional[int]
    data: Optional[str]


class TGetUpdatesResult(BaseModel):
    update_id: int
    message: Optional[TGetUpdatesResultMessage]
    callback_query: Optional[TGetUpdatesResultCallBackQuery]


class TGetUpdates(BaseModel):
    ok: bool
    result: Optional[List[TGetUpdatesResult]]


class Handle(ABC):
    message: TGetUpdatesResult = None
    chat_id: int

    def __init__(self, message):
        self.message = message
        self.chat_id = message.message.from_.id

    def do(self):
        self.run()

    @abstractmethod
    def run(self):
        pass


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

    def register_handler(self, command: str, f: Handle):
        com = command if command.startswith('/') else '/' + command
        self.handlers[com] = f

    def message_handle(self, state=None, command=None):
        if state:
            def wrapper_state(c):
                self.handlers[state] = c
                return c

            return wrapper_state

        if command:
            com = command if command.startswith('/') else '/' + command

            def wrapper_command(c):
                self.handlers[com] = c
                return c

            return wrapper_command

    def _get_handlers(self, message: TGetUpdatesResult):
        command = message.message.text
        if self.is_command(self, command):
            handle = self.handlers.get(command)
            if handle:
                h = handle(message)
                return h.do()

        chat_id = message.message.from_.id
        user = self.data.get_user(chat_id)
        user_state = user.state
        handle = self.handlers.get(user_state)
        if handle:
            h = handle(message)
            return h.do()

    @staticmethod
    def is_command(cls, command: str):
        return True if command.startswith('/') else False

    def polling(self):
        data = self.get_updates().json()
        get_updates = TGetUpdates(**data)
        if get_updates.ok:
            for update in get_updates.result:
                update_id = self.data.get_update_id()
                if update.update_id > update_id:
                    self.data.set_update_id(update.update_id)
                    self._get_handlers(update)

    def run(self):
        try:
            while True:
                self.polling()
                sleep(0.5)
        except KeyboardInterrupt:
            print("Stop bot")
