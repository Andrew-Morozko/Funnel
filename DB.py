id_converter = {
    'VK2Telegram': {
        # <vk id>: (<Telegram group id>, False)
        0: (0, False)
    },
    'Telegram2VK': {
        # <Telegram group id>: (<vk id>, False)
        0: (0, False)
    }

}


# TODO: replace with sqlite db
def convert_ids(source, dest, source_id, need_group_info=False):
    """ Returns tuple (dest_id, is_group) or just dest_id. None on errors"""
    try:
        info = id_converter['{}2{}'.format(source, dest)][source_id]
        if need_group_info:
            return info
        else:
            return info[0]
    except:
        return None

"""
DB: vkid(int), telegramid(int), send_name(bool) // send_name - show names in group chats
Magic record: vkid(0), telegramid(xxx), send_name(true) // catch-all telegram chat
Request: select * where vkid==*vkid* or vkid==0
If returned 2 records – use one with vkid==vkid
1 – use catch-all

Function returnes tuple: (telegramid, send_name)
"""
