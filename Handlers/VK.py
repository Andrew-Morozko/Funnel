import requests
import threading
import Handler
import json
import sys


class VKConn(object):
    """ Connection to server """

    def __init__(self, token, api_version):
        self.__rate_limiter = threading.Lock()

        self.required_params = {"access_token": token, "v": api_version}

        self.longpoll_data = {}

    def __make_request(self, *args, **kwargs):
        """ Wraps requests.request with thread-aware delay function """

        self.__rate_limiter.acquire()
        r = requests.request(*args, **kwargs)
        threading.Timer(0.4, self.__rate_limiter.release).start()

        return r

    def api_request(self, api_method, params):
        params.update(self.required_params)

        result = self.__make_request(url="https://api.vk.com/method/" + api_method,
                                     method="POST", params=params, timeout=5).json()

        if __debug__:
            print("VK Request: " + api_method, file=sys.stderr)
            print(json.dumps(params, indent=4, sort_keys=True), file=sys.stderr)
            print("Response: " + api_method, file=sys.stderr)
            print(json.dumps(result, indent=4, sort_keys=True), file=sys.stderr)

        return result

    def longpoll(self, ts):
        """ Not threadsave, should be used only by Handler thread """
        if not self.longpoll_data:
            raise ValueError('No longpoll data!')

        return requests.get("http://{server}?act=a_check&key={key}&ts={ts}&wait=25&mode=2"
                            .format(**self.longpoll_data, ts=ts), timeout=50).json()


class VK(Handler.Handler):
    def __init__(self, VKToken):
        self.conn = VKConn(token=VKToken, api_version=5.44)

        super(VK, self).__init__()

    # Receives messages from vk
    def receiver(self, q):

        ts = self.init_longpoll()

        while True:

            resp = self.conn.longpoll(ts)

            if __debug__:
                print(resp, file=sys.stderr)

            # Error handling. TODO: log this
            if 'failed' in resp:

                if __debug__:
                    print(json.dumps(resp, indent=4, sort_keys=True), file=sys.stderr)

                if resp['failed'] == 1:
                    """ Server error, continue with new TS """
                    ts = resp['ts']
                    continue

                elif resp['failed'] == 2:
                    """ Longpoll key expired, get new and continue with old ts """
                    _ = self.init_longpoll()
                    continue

                elif resp['failed'] == 3:
                    """ Something seriously bugged out, get new key and server, start with new ts """
                    ts = self.init_longpoll()
                    continue

                else:
                    """ Unknown error, shutdown """
                    pass  # TODO: implement

            # Processing resp

            for upd in resp['updates']:
                q.put(upd, block=False)

            ts = resp['ts']  # Swiching to next update

    def init_longpoll(self):
        """ Returns ts or dies! """

        longpoll_data = self.conn.api_request('messages.getLongPollServer', {'use_ssl': 1, 'need_pts': 0})

        # TODO: error handling. Just send error message to log and shutdown.
        # TODO: create tcp server for logging (example in logger dir)

        longpoll_data = longpoll_data['response']

        self.conn.longpoll_data['server'] = longpoll_data['server']
        self.conn.longpoll_data['key']    = longpoll_data['key']

        if __debug__:
            print("Done init_longpoll()", file=sys.stderr)

        return longpoll_data['ts']

    # Sends messages to vk
    def sender(self, q):
        while True:
            msg = q.get(block=True)
            self.conn.api_request(**msg)
            # TODO: Error handling
