from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext, Updater

import config
from mode_data.group import BJgroup
from mode_fun.msgdel import msgdel, keyboard_msgdel
from mode_user.user import BJuser


async def set_callback(update: Update, context: CallbackContext):
    chat = update.callback_query.message.chat
    user = update.callback_query.from_user

    username = 'CCNULL'
    if user.username:
        username = user.username
    myuser = BJuser(user.id, user.first_name, username)

    if not myuser.id == config.author:
        if not myuser.groupadmin(chat.id):
            await update.callback_query.answer()
            return

    markup = [
        [
            InlineKeyboardButton(text='🎲 删除自身指令', callback_data='group_set_null'),
            InlineKeyboardButton(text='✅ 是', callback_data='group_set_del_com')
        ],
        [
            InlineKeyboardButton(text='🔮 删除通知信息', callback_data='group_set_null'),
            InlineKeyboardButton(text='✅ 是', callback_data='group_set_del_chat')
        ],
        [
            InlineKeyboardButton(text='🎭 删除所有指令', callback_data='group_set_null'),
            InlineKeyboardButton(text='❎ 否', callback_data='group_set_del_allcom')
        ],
        [
            InlineKeyboardButton(text='🛸退出', callback_data='group_set_back'),
        ]
    ]

    if update.callback_query.data == 'group_set_null':
        await update.callback_query.answer()
        return

    elif update.callback_query.data == 'group_set_back':
        await update.callback_query.answer()
        await keyboard_msgdel(update, context)
        return

    mygroup = BJgroup(chat.id, chat.title)

    if update.callback_query.data == 'group_set_del_com':
        if mygroup.del_com == 1:
            mygroup.set('del_com', 0)
            if mygroup.del_allcom == 1:
                mygroup.set('del_allcom', 0)
        else:
            mygroup.set('del_com', 1)

    elif update.callback_query.data == 'group_set_del_chat':
        if mygroup.del_chat == 1:
            mygroup.set('del_chat', 0)
        else:
            mygroup.set('del_chat', 1)

    elif update.callback_query.data == 'group_set_del_allcom':
        if mygroup.del_allcom == 1:
            mygroup.set('del_allcom', 0)
        else:
            mygroup.set('del_allcom', 1)

        if mygroup.del_com == 0:
            mygroup.set('del_com', 1)

    await update.callback_query.answer()

    if not mygroup.del_com:
        markup[0][1] = InlineKeyboardButton(text='❎ 否', callback_data='group_set_del_com')
    if not mygroup.del_chat:
        markup[1][1] = InlineKeyboardButton(text='❎ 否', callback_data='group_set_del_chat')
    if mygroup.del_allcom:
        markup[2][1] = InlineKeyboardButton(text='✅ 是', callback_data='group_set_del_allcom')

    reply_markup = InlineKeyboardMarkup(markup)
    try:
        await update.callback_query.message.edit_reply_markup(reply_markup)
    except Exception as e:
        print(repr(e))
    return


async def group_set(update: Update, context: CallbackContext):
    chat = update.effective_chat
    user = update.effective_user

    await msgdel(update, context)

    if not chat.type == 'private':
        username = 'CCNULL'
        if user.username:
            username = user.username
        myuser = BJuser(user.id, user.first_name, username)

        if not myuser.id == config.author:
            if not myuser.groupadmin(chat.id):
                return

        mygroup = BJgroup(chat.id, chat.title)
        markup = [
            [
                InlineKeyboardButton(text='🎲 删除自身指令', callback_data='group_set_null'),
                InlineKeyboardButton(text='✅ 是', callback_data='group_set_del_com')
            ],
            [
                InlineKeyboardButton(text='🔮 删除通知信息', callback_data='group_set_null'),
                InlineKeyboardButton(text='✅ 是', callback_data='group_set_del_chat')
            ],
            [
                InlineKeyboardButton(text='🎭 删除所有指令', callback_data='group_set_null'),
                InlineKeyboardButton(text='❎ 否', callback_data='group_set_del_allcom')
            ],
            [
                InlineKeyboardButton(text='🛸退出', callback_data='group_set_back'),
            ]
        ]
        if not mygroup.del_com:
            markup[0][1] = InlineKeyboardButton(text='❎ 否', callback_data='group_set_del_com')
        if not mygroup.del_chat:
            markup[1][1] = InlineKeyboardButton(text='❎ 否', callback_data='group_set_del_chat')
        if mygroup.del_allcom:
            markup[2][1] = InlineKeyboardButton(text='✅ 是', callback_data='group_set_del_allcom')

        reply_markup = InlineKeyboardMarkup(markup)
        await context.bot.sendMessage(
            chat.id, "🕹喜仔配置（简洁版\n\nTip:开启功能之前请给予对应权限", reply_markup=reply_markup
        )
        return
