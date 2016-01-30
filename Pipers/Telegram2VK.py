import Piper
import html
import os
import DB


class Telegram2VK(Piper.Piper):
    def __init__(self, source, dest):
        """ Gets 2 handlers """
        super(Telegram2VK, self).__init__(source, dest)

    def converter(self, in_q, out_q):
        while True:
            telegram_msg = in_q.get(block=True)

            if 'message' in telegram_msg:  # New message
                if 'text' not in telegram_msg['message']:
                    continue

                vk_id = DB.convert_ids('Telegram', 'VK', telegram_msg['message']['chat']['id'])

                if vk_id is None:
                    continue

                vk_msg = {'api_method': 'messages.send', 'params': {}}
                vk_msg['params']['peer_id'] = vk_id
                vk_msg['params']['message'] = telegram_msg['message']['text']

                out_q.put(vk_msg)

            # else:
            #     discarding the message
