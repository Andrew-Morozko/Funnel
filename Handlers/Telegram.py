import requests
import threading
import Handler
import json
import sys


class TelegramConn(object):
    """ Connection to server """

    def __init__(self, token):
        self.base_url = "https://api.telegram.org/bot{}/".format(token)

    def __make_request(self, *args, **kwargs):
        """ Wraps requests.request """
        """
            30 msg/sec is a very high limit, considering that threads are limited
            to 1 msg per 3 sec, so there is no global rate limiter.
            Nevertheless, there is handling for http response 429 (Too Many Requests)
        """

        r = requests.request(*args, **kwargs)

        if r.status_code == 429:
            import time
            time.sleep(5)
            r = requests.request(*args, **kwargs)

        return r

    def api_request(self, api_method, params, timeout=5):
        result = self.__make_request(url=self.base_url + api_method, method="POST",
                                     params=params, timeout=timeout).json()

        if __debug__:
            print("Telegram Request: " + api_method, file=sys.stderr)
            print(json.dumps(params, indent=4, sort_keys=True), file=sys.stderr)
            print("Response: " + api_method, file=sys.stderr)
            print(json.dumps(result, indent=4, sort_keys=True), file=sys.stderr)

        return result

    def longpoll(self, last_offset=0):
        """ Not threadsave, should be used only by Handler thread """

        params = {'timeout': 25}

        if last_offset != 0:
            params['offset'] = last_offset + 1

        return self.api_request('getUpdates', params=params, timeout=50)


class Telegram(Handler.Handler):
    def __init__(self, TelegramToken):
        self.conn = TelegramConn(token=TelegramToken)

        super(Telegram, self).__init__()

    # Receives messages from Telegram
    def receiver(self, q):
        last_offset = 0
        while True:
            resp = self.conn.longpoll(last_offset)
            if not resp['ok']:
                # Error handling
                continue

            for upd in resp['result']:
                if upd['update_id'] > last_offset:
                    last_offset = upd['update_id']
                q.put(upd)

    # Sends messages to Telegram
    def sender(self, q):
        while True:
            msg = q.get(block=True)
            self.conn.api_request('sendMessage', msg)
