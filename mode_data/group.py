from telegram import Update
from telegram.ext import CallbackContext

from mode_data.database import group_seach, group_set


class BJgroup:
    def __init__(self, group_id, group_name):
        self.group_id = group_id
        self.group_name = group_name
        data = group_seach(group_id, group_name)
        # print(data)
        self.del_com = data[0]
        self.del_chat = data[1]
        self.del_allcom = data[2]

    def update(self):
        data = group_seach(self.group_id, self.group_name)
        self.del_com = data[0]
        self.del_chat = data[1]
        self.del_allcom = data[2]

    def set(self, mode, value):
        group_set(self.group_id, mode, value)
        if mode == 'del_com':
            self.del_com = value
        elif mode == 'del_chat':
            self.del_chat = value
        elif mode == 'del_allcom':
            self.del_allcom = value


def build_group_msg(update: Update) -> BJgroup:
    chat = update.effective_chat

    mygroup = BJgroup(chat.id, chat.title)
    return mygroup


def build_group_callback(context: CallbackContext) -> BJgroup:
    chat = context.job.context.chat

    mygroup = BJgroup(chat.id, chat.title)
    return mygroup

