from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.constants import ParseMode
from telegram.ext import CallbackContext
from telegram.helpers import escape_markdown

import config
from mode_data.database import set_conn, user_add
from mode_data.write_txt import admin_write
from mode_fun.msgdel import msgdel, auto_msgdel
from mode_user.user import BJuser


def add_admin(user_id, name, username) -> bool:
    conn = set_conn()
    cursor = conn.cursor()
    results = 0
    sql = "UPDATE user SET admin=1 WHERE id={}".format(user_id)
    try:
        results = cursor.execute(sql)
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(repr(e))
    if not results:
        if user_add(user_id, name, username):
            add_admin(user_id, name, username)
            return True
        else:
            return False
    conn.close()
    admin_write('[新增大喜仔] UID:{} NA:{} UN:{}'.format(user_id, name, username))
    return True


def del_admin(user_id) -> bool:
    conn = set_conn()
    cursor = conn.cursor()
    results = 0
    sql = "UPDATE user SET admin=0 WHERE id={}".format(user_id)
    try:
        results = cursor.execute(sql)
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(repr(e))
    conn.close()
    if not results:
        return False
    admin_write('[删除大喜仔] UID:{}'.format(user_id))
    return True


def ban_user(user_id, name='CC小可爱', username='CC小可爱', ban_text='CC小可爱', ban_admin='CC') -> bool:
    conn = set_conn()
    cursor = conn.cursor()
    results = 0
    sql = "UPDATE user SET `ban`=1,`ban_text`='{}',`ban_admin`='{}' WHERE id={}".format(ban_text, ban_admin, user_id)
    try:
        results = cursor.execute(sql)
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(repr(e))
    if not results:
        if not user_add(user_id, name, username):
            return False
        ban_user(user_id, name, username, ban_text, ban_admin)
    conn.close()
    return True


def unban_user(user_id) -> bool:
    conn = set_conn()
    cursor = conn.cursor()
    sql = "UPDATE user SET `ban`=0 WHERE `id`={}".format(user_id)
    try:
        cursor.execute(sql)
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(repr(e))
    conn.close()
    return True


def do_setpia(user_id, num) -> bool:
    conn = set_conn()
    cursor = conn.cursor()
    results = 0
    sql = "UPDATE user SET pia_num={} WHERE id={}".format(num, user_id)
    try:
        results = cursor.execute(sql)
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(repr(e))
    conn.close()
    if not results:
        return False
    admin_write('[更改大逼兜权重] UID:{} Power:{}'.format(user_id, num))
    return True


async def ccadd(update: Update, context: CallbackContext):
    msg = update.effective_message
    chat = update.effective_chat
    user = update.effective_user

    backmsg = ''

    username = 'CCNULL'
    if user.username:
        username = user.username
    myuser = BJuser(user.id, user.first_name, username)

    if myuser.id == config.author:
        if msg.reply_to_message:
            if chat.type == 'private':
                await context.bot.sendMessage(chat_id=chat.id, text='🎊 Cc你好~')
            else:
                touser_name = msg.reply_to_message.from_user.first_name
                touser_id = msg.reply_to_message.from_user.id
                touser_username = msg.reply_to_message.from_user.username
                if not touser_username:
                    touser_username = 'CCNULL'
                if add_admin(touser_id, touser_name, touser_username):
                    await context.bot.sendMessage(
                        chat_id=chat.id,
                        text='🥳 [{}](tg://user?id={})已被任命为*大喜仔*'.format(
                            escape_markdown(touser_name, version=2), touser_id
                        ), parse_mode=ParseMode.MARKDOWN_V2)
                else:
                    backmsg = await context.bot.sendMessage(
                        chat_id=chat.id,
                        text='🤯 任命*大喜仔*失败', parse_mode=ParseMode.MARKDOWN_V2)
        else:
            backmsg = await context.bot.sendMessage(
                chat_id=chat.id,
                text='🎊 呆瓜Cc你好~')
    else:
        backmsg = await context.bot.sendMessage(
            chat_id=chat.id,
            text='[{}](tg://user?id={}) ，你个假Cc！！！'.format(
                escape_markdown(myuser.name, version=2), myuser.id
            ), parse_mode=ParseMode.MARKDOWN_V2)
    await msgdel(update, context)
    if backmsg and not chat.type == 'private':
        context.job_queue.run_once(auto_msgdel, 5, data={
            'bot': context.bot,
            'chat':backmsg.chat,
            'message_id': backmsg.message_id
        })


async def ccdel(update: Update, context: CallbackContext):
    msg = update.effective_message
    chat = update.effective_chat
    user = update.effective_user

    backmsg = ''

    username = 'CCNULL'
    if user.username:
        username = user.username
    myuser = BJuser(user.id, user.first_name, username)

    if myuser.id == config.author:
        if msg.reply_to_message:
            if chat.type == 'private':
                await context.bot.sendMessage(
                    chat_id=chat.id,
                    text='🎊 Cc你好~')
            else:
                touser_name = msg.reply_to_message.from_user.first_name
                touser_id = msg.reply_to_message.from_user.id
                if del_admin(touser_id):
                    await context.bot.sendMessage(
                        chat_id=chat.id,
                        text='🥳 [{}](tg://user?id={})已毕业，不再是*大喜仔*'.format(
                            escape_markdown(touser_name, version=2), touser_id
                        ),
                        parse_mode=ParseMode.MARKDOWN_V2)
                else:
                    backmsg = await context.bot.sendMessage(
                        chat_id=chat.id,
                        text='🤯 *毕业失败*', parse_mode=ParseMode.MARKDOWN_V2)
        else:
            backmsg = await context.bot.sendMessage(
                chat_id=chat.id,
                text='😑 呆瓜Cc')
    else:
        backmsg = await context.bot.sendMessage(
            chat_id=chat.id,
            text='[{}](tg://user?id={}) ，你个假Cc！！！'.format(
                escape_markdown(myuser.name, version=2), myuser.id
            ), parse_mode=ParseMode.MARKDOWN_V2)
    if backmsg and not chat.type == 'private':
        context.job_queue.run_once(auto_msgdel, 5, data={
            'bot': context.bot,
            'chat':backmsg.chat,
            'message_id': backmsg.message_id
        })


async def setpia(update: Update, context: CallbackContext):
    msg = update.effective_message
    chat = update.effective_chat
    user = update.effective_user

    username = 'CCNULL'
    if user.username:
        username = user.username
    myuser = BJuser(user.id, user.first_name, username)

    if myuser.id == config.author:
        pia_num = msg.text.replace(config.bot['name'], '')
        if not len(pia_num) > len('/setpia '):
            backmsg = await context.bot.sendMessage(
                chat_id=chat.id,
                text="😑 呆瓜Cc")
            await msgdel(update, context)
            if not chat.type == 'private':
                context.job_queue.run_once(auto_msgdel, 5, data={
                    'bot': context.bot,
                    'chat':backmsg.chat,
                    'message_id': backmsg.message_id
                })
            return
        else:
            pia_num = pia_num[len('/rename '):].strip()

        if msg.reply_to_message:
            touser_name = msg.reply_to_message.from_user.first_name
            touser_id = msg.reply_to_message.from_user.id
            if do_setpia(touser_id, int(pia_num)):
                backmsg = await context.bot.sendMessage(
                    chat_id=chat.id,
                    text='🥳 [{}](tg://user?id={})的大逼兜权重已更改为 *{}*'.format(
                        escape_markdown(touser_name, version=2), touser_id,
                        escape_markdown(pia_num, version=2)
                    ), parse_mode=ParseMode.MARKDOWN_V2)
            else:
                backmsg = await context.bot.sendMessage(
                    chat_id=chat.id,
                    text='🤯 [{}](tg://user?id={})的大逼兜权重更改失败'.format(
                        escape_markdown(touser_name, version=2), touser_id
                    ), parse_mode=ParseMode.MARKDOWN_V2)
        else:
            if do_setpia(myuser.id, int(pia_num)):
                backmsg = await context.bot.sendMessage(
                    chat_id=chat.id,
                    text='🥳 [{}](tg://user?id={})的大逼兜权重已更改为 *{}*'.format(
                        escape_markdown(myuser.name, version=2), myuser.id,
                        escape_markdown(pia_num, version=2)
                    ), parse_mode=ParseMode.MARKDOWN_V2)
            else:
                backmsg = await context.bot.sendMessage(
                    chat_id=chat.id,
                    text='🤯 [{}](tg://user?id={})的大逼兜权重更改失败'.format(
                        escape_markdown(myuser.name, version=2), myuser.id
                    ), parse_mode=ParseMode.MARKDOWN_V2)
    else:
        backmsg = await context.bot.sendMessage(
            chat_id=chat.id,
            text='💣 笨蛋[{}](tg://user?id={}) ，这个命令只有Cc可用'.format(
                escape_markdown(myuser.name, version=2), myuser.id
            ), parse_mode=ParseMode.MARKDOWN_V2)
    await msgdel(update, context)
    if backmsg and not chat.type == 'private':
        context.job_queue.run_once(auto_msgdel, 5, data={
            'bot': context.bot,
            'chat':backmsg.chat,
            'message_id': backmsg.message_id
        })


async def ccban(update: Update, context: CallbackContext):
    msg = update.effective_message
    chat = update.effective_chat
    user = update.effective_user

    backmsg = ''

    username = 'CCNULL'
    if user.username:
        username = user.username
    myuser = BJuser(user.id, user.first_name, username)

    if myuser.id == config.author:
        if msg.reply_to_message:

            ban_text = msg.text.replace(config.bot['name'], '')
            if not len(ban_text) > len('/hot '):
                ban_text = "无理由"
            else:
                ban_text = ban_text[len('/hot '):].strip()

            if chat.type == 'private':
                await context.bot.sendMessage(
                    chat_id=chat.id,
                    text='🎊 Cc你好~')
            else:
                touser_name = msg.reply_to_message.from_user.first_name
                touser_id = msg.reply_to_message.from_user.id
                touser_username = msg.reply_to_message.from_user.username
                if not touser_username:
                    touser_username = 'CCNULL'
                if ban_user(touser_id, touser_name, touser_username, ban_text, myuser.id):
                    await context.bot.sendMessage(
                        chat_id=chat.id,
                        text='🥳 [{}](tg://user?id={})已被[{}](tg://user?id={})*封禁*'.format(
                            escape_markdown(touser_name, version=2), touser_id,
                            escape_markdown(myuser.name, version=2), myuser.id
                        ), parse_mode=ParseMode.MARKDOWN_V2)
                else:
                    backmsg = await context.bot.sendMessage(
                        chat_id=chat.id,
                        text='🤯 *封禁*失败', parse_mode=ParseMode.MARKDOWN_V2)
        else:
            backmsg = await context.bot.sendMessage(
                chat_id=chat.id,
                text='🎊 呆瓜Cc你好~')
    else:
        backmsg = await context.bot.sendMessage(
            chat_id=chat.id,
            text='[{}](tg://user?id={})想被ban？'.format(
                escape_markdown(myuser.name, version=2), myuser.id
            ), parse_mode=ParseMode.MARKDOWN_V2)
    await msgdel(update, context)
    if backmsg and not chat.type == 'private':
        context.job_queue.run_once(auto_msgdel, 5, data={
            'bot': context.bot,
            'chat':backmsg.chat,
            'message_id': backmsg.message_id
        })


async def ccunban(update: Update, context: CallbackContext):
    msg = update.effective_message
    chat = update.effective_chat
    user = update.effective_user

    backmsg = ''

    username = 'CCNULL'
    if user.username:
        username = user.username
    myuser = BJuser(user.id, user.first_name, username)

    if myuser.id == config.author:
        if msg.reply_to_message:
            if chat.type == 'private':
                await context.bot.sendMessage(chat_id=chat.id, text='🎊 Cc你好~')
            else:
                touser_name = msg.reply_to_message.from_user.first_name
                touser_id = msg.reply_to_message.from_user.id
                if unban_user(touser_id):
                    await context.bot.sendMessage(
                        chat_id=chat.id,
                        text='🥳 [{}](tg://user?id={})已被*解封*'.format(
                            escape_markdown(touser_name, version=2), touser_id,
                        ), parse_mode=ParseMode.MARKDOWN_V2)
                else:
                    backmsg = await context.bot.sendMessage(
                        chat_id=chat.id, text='🤯 *解封*失败', parse_mode=ParseMode.MARKDOWN_V2)
        else:
            backmsg = await context.bot.sendMessage(
                chat_id=chat.id,
                text='🎊 呆瓜Cc你好~')
    else:
        backmsg = await context.bot.sendMessage(
            chat_id=chat.id,
            text='[{}](tg://user?id={})想被ban？'.format(
                escape_markdown(myuser.name, version=2), myuser.id
            ), parse_mode=ParseMode.MARKDOWN_V2)
    await msgdel(update, context)
    if backmsg and not chat.type == 'private':
        context.job_queue.run_once(auto_msgdel, 5, data={
            'bot': context.bot,
            'chat':backmsg.chat,
            'message_id': backmsg.message_id
        })


async def cc_pro(update: Update, context: CallbackContext):
    chat = update.effective_chat
    # print(msg.text)
    await msgdel(update, context)
    reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text='确定', callback_data='back'),
            ],
            [
                InlineKeyboardButton(text='返回', callback_data='back'),
            ],
        ]
    )
    await context.bot.sendMessage(chat_id=chat.id, text="Cc你好吖", reply_markup=reply_markup)
    return
