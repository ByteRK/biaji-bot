import requests

import config


def checkgroup(userid, chatgroup_id) -> bool:
    url = "https://api.telegram.org/bot" + \
          config.bot['key'] + "/getChatMember?chat_id=" + str(chatgroup_id) + "&user_id=" + str(userid)
    response = requests.get(url)
    data = response.json()
    if not data["ok"]:
        return False
    if data["result"]["status"] not in ("member", "administrator", "creator"):
        return False
    else:
        return True


def checkgroupadmin(userid, chatgroup_id) -> bool:
    url = "https://api.telegram.org/bot" + \
          config.bot['key'] + "/getChatMember?chat_id=" + str(chatgroup_id) + "&user_id=" + str(userid)
    response = requests.get(url)
    data = response.json()
    if not data["ok"]:
        return False
    if data["result"]["status"] not in ("administrator", "creator"):
        return False
    else:
        return True


if __name__ == '__main__':
    # ccadd(11, '66', '55')
    Bot_API = "5245812142:AAG7hfPdJF_8XB7V5htmgt_G6hn1kNoiif0"
    print(checkgroupadmin(5577400096, -1001518926694))
