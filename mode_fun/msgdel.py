from telegram import Update
from telegram.ext import Updater, CallbackContext

import config
from mode_data.group import build_group_msg, build_group_callback


def msgdel(update: Update):
    if not update.message.chat.type == 'private':
        mygroup = build_group_msg(update)
        if not mygroup.del_com:
            return
        try:
            Updater(
                config.bot['key'],
                request_kwargs={
                    'proxy_url': config.proxy
                }
            ).bot.delete_message(
                chat_id=update.message.chat_id,
                message_id=update.message.message_id
            )
        except Exception as e:
            print(repr(e))
            # tgbot.bot.sendMessage(update.message.chat_id, '可以把我设置为管理员进行删除指令哦')


def auto_msgdel(context: CallbackContext):
    mygroup = build_group_callback(context)
    if not mygroup.del_chat:
        return
    try:
        context.bot.delete_message(
            chat_id=context.job.context.chat.id,
            message_id=context.job.context.message_id
        )
    except Exception as e:
        print(repr(e))


def keyboard_msgdel(update: Update):
    try:
        Updater(
            config.bot['key'],
            request_kwargs={
                'proxy_url': config.proxy
            }
        ).bot.delete_message(
            chat_id=update.callback_query.message.chat.id,
            message_id=update.callback_query.message.message_id
        )
    except Exception as e:
        print(repr(e))


def all_comdel(update: Update, context: CallbackContext):
    if not update.message.chat.type == 'private':
        mygroup = build_group_msg(update)
        if not mygroup.del_allcom:
            return
        try:
            context.bot.delete_message(
                chat_id=update.message.chat_id,
                message_id=update.message.message_id
            )
        except Exception as e:
            print(repr(e))
            # tgbot.bot.sendMessage(update.message.chat_id, '可以把我设置为管理员进行删除指令哦')
