import Piper
import html
import os
import DB


class VK2Telegram(Piper.Piper):
    def __init__(self, source, dest):
        """ Gets 2 handlers """
        super(VK2Telegram, self).__init__(source, dest)

    def converter(self, in_q, out_q):
        while True:
            vk_msg = in_q.get(block=True)

            if vk_msg[0] == 4:  # New message
                if vk_msg[2] & 2:  # Flag 'OUTBOX' set
                    continue

                telegram_info = DB.convert_ids('VK', 'Telegram', vk_msg[3], need_group_info=True)

                if telegram_info is None:
                    continue

                telegram_msg = {'parse_mode': "HTML"}
                telegram_msg['chat_id'] = telegram_info[0]

                if telegram_info[1]:
                    telegram_msg['text'] = "<b>Name Placeholder</b>:\n"
                else:
                    telegram_msg['text'] = ""

                telegram_msg['text'] += vk_msg[6].replace('<br>', '\n')
                out_q.put(telegram_msg)

            # else:
            #     discarding the message
