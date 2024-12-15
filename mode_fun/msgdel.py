from telegram import Update
from telegram.ext import Updater, CallbackContext

import config
from mode_data.group import build_group_msg, build_group_callback


async def msgdel(update: Update, context: CallbackContext):
    if not update.message.chat.type == 'private':
        mygroup = build_group_msg(update)
        if not mygroup.del_com:
            return
        try:
            await context.bot.delete_message(
                chat_id=update.message.chat_id,
                message_id=update.message.message_id
            )
        except Exception as e:
            print(repr(e))
            # tgbot.bot.sendMessage(update.message.chat_id, '可以把我设置为管理员进行删除指令哦')


async def auto_msgdel(context):
    data = context.job.data
    chat = data["chat"]
    mygroup = build_group_callback(chat.id, chat.title)
    if not mygroup.del_chat:
        return
    try:
        await data["bot"].delete_message(
            chat_id=chat.id,
            message_id=data["message_id"]
        )
    except Exception as e:
        print(repr(e))


async def keyboard_msgdel(update: Update, context: CallbackContext):
    try:
        await context.bot.delete_message(
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
