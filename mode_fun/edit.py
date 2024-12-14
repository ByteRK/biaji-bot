from telegram import Update, ParseMode
from telegram.ext import CallbackContext
from telegram.utils.helpers import escape_markdown

import config
from mode_user.user import BJuser
from mode_data.database import do_rename, do_unrename, do_repia, do_unrepia
from mode_fun.msgdel import msgdel, auto_msgdel


def rename(update: Update, context: CallbackContext):
    msg = update.effective_message
    chat = update.effective_chat
    user = update.effective_user

    backmsg = ''

    rename_text = msg.text.replace(config.bot['name'], '')
    if not len(rename_text) > len('/rename '):
        backmsg = context.bot.sendMessage(
                        chat_id=chat.id,
                        text="🐷 命令使用错误")
        msgdel(update)
        if not chat.type == 'private':
            context.job_queue.run_once(auto_msgdel, 5, context=backmsg)
        return
    else:
        rename_text = rename_text[len('/rename '):].strip()

    username = 'CCNULL'
    if user.username:
        username = user.username
    myuser = BJuser(user.id, user.first_name, username)

    if myuser.ban:
        backmsg = context.bot.sendMessage(
                        chat_id=chat.id,
                        text='[{}](tg://user?id={})已经被{}了'.format(
                            escape_markdown(myuser.name, version=2), myuser.id,
                            escape_markdown("打(Feng)傻(Jing)", version=2)
                        ), parse_mode=ParseMode.MARKDOWN_V2)
        msgdel(update)
        if not chat.type == 'private':
            context.job_queue.run_once(auto_msgdel, 8, context=backmsg)
        return

    if msg.reply_to_message:
        if myuser.admin:
            if myuser.id != 570255200 and msg.reply_to_message.from_user.id == 570255200:
                context.bot.sendMessage(
                    chat_id=chat.id,
                    text='😡 抓到[{}](tg://user?id={})想改[Cc](tg://user?id=570255200)的名字！！！'.format(
                        escape_markdown(myuser.name, version=2), myuser.id
                    ), parse_mode=ParseMode.MARKDOWN_V2)
            else:
                touser_name = msg.reply_to_message.from_user.first_name
                touser_id = msg.reply_to_message.from_user.id
                touser_username = msg.reply_to_message.from_user.username
                if not touser_username:
                    touser_username = 'CCNULL'
                if do_rename(touser_id, touser_name, touser_username, rename_text):
                    backmsg = context.bot.sendMessage(
                        chat_id=chat.id,
                        text='🎀 [{}](tg://user?id={})已更改喜仔名为 *{}*'.format(
                            escape_markdown(touser_name, version=2), touser_id, escape_markdown(rename_text, version=2)
                        ), parse_mode=ParseMode.MARKDOWN_V2)
                else:
                    backmsg = context.bot.sendMessage(
                        chat_id=chat.id,
                        text='🚨 改名失败')
        else:
            backmsg = context.bot.sendMessage(
                        chat_id=chat.id,
                        text='🚧 [{}](tg://user?id={})非大喜仔,无法修改他人昵称'.format(
                            escape_markdown(myuser.name, version=2), myuser.id
                        ), parse_mode=ParseMode.MARKDOWN_V2)
    elif not msg.reply_to_message and myuser.admin:
        if do_rename(myuser.id, myuser.name, myuser.username, rename_text):
            backmsg = context.bot.sendMessage(
                        chat_id=chat.id,
                        text='🎀 [{}](tg://user?id={})已更改喜仔名为 *{}*'.format(
                            escape_markdown(myuser.name, version=2), myuser.id, escape_markdown(rename_text, version=2)
                        ), parse_mode=ParseMode.MARKDOWN_V2)
        else:
            backmsg = context.bot.sendMessage(
                        chat_id=chat.id,
                        text='🚨 改名失败')
    else:
        backmsg = context.bot.sendMessage(
                        chat_id=chat.id,
                        text='🚧 [{}](tg://user?id={})非大喜仔,无自定义昵称权限'.format(
                            escape_markdown(myuser.name, version=2), myuser.id
                        ), parse_mode=ParseMode.MARKDOWN_V2)

    msgdel(update)
    if backmsg and not chat.type == 'private':
        context.job_queue.run_once(auto_msgdel, 8, context=backmsg)


def unrename(update: Update, context: CallbackContext):
    msg = update.effective_message
    chat = update.effective_chat
    user = update.effective_user

    backmsg = ''

    username = 'CCNULL'
    if user.username:
        username = user.username
    myuser = BJuser(user.id, user.first_name, username)

    if myuser.ban:
        backmsg = context.bot.sendMessage(
                        chat_id=chat.id,
                        text='[{}](tg://user?id={})已经被{}了'.format(
                            escape_markdown(myuser.name, version=2), myuser.id,
                            escape_markdown("打(Feng)傻(Jing)", version=2)
                        ), parse_mode=ParseMode.MARKDOWN_V2)
        msgdel(update)
        if not chat.type == 'private':
            context.job_queue.run_once(auto_msgdel, 8, context=backmsg)
        return

    if msg.reply_to_message:
        if myuser.admin:
            if myuser.id != 570255200 and msg.reply_to_message.from_user.id == 570255200:
                context.bot.sendMessage(
                        chat_id=chat.id,
                        text='😡 抓到[{}](tg://user?id={})想改[Cc](tg://user?id=570255200)的名字！！！'.format(
                            escape_markdown(myuser.name, version=2), myuser.id
                        ), parse_mode=ParseMode.MARKDOWN_V2)
            else:
                touser_name = msg.reply_to_message.from_user.first_name
                touser_id = msg.reply_to_message.from_user.id
                if do_unrename(touser_id):
                    backmsg = context.bot.sendMessage(
                        chat_id=chat.id,
                        text='🎀 [{}](tg://user?id={})已关闭*喜仔名*'.format(
                            escape_markdown(touser_name, version=2), touser_id
                        ), parse_mode=ParseMode.MARKDOWN_V2)
                else:
                    backmsg = context.bot.sendMessage(
                        chat_id=chat.id,
                        text='🚨 关闭*喜仔名*失败', parse_mode=ParseMode.MARKDOWN_V2)
        else:
            backmsg = context.bot.sendMessage(
                        chat_id=chat.id,
                        text='🚧 [{}](tg://user?id={})非大喜仔,无法修改他人昵称'.format(
                            escape_markdown(myuser.name, version=2), myuser.id
                        ), parse_mode=ParseMode.MARKDOWN_V2)
    elif not msg.reply_to_message and myuser.admin:
        if do_unrename(myuser.id):
            backmsg = context.bot.sendMessage(
                        chat_id=chat.id,
                        text='🎀 [{}](tg://user?id={})已关闭*喜仔名*'.format(
                            escape_markdown(myuser.name, version=2), myuser.id
                        ), parse_mode=ParseMode.MARKDOWN_V2)
        else:
            backmsg = context.bot.sendMessage(
                        chat_id=chat.id,
                        text='🚨 关闭*喜仔名*失败', parse_mode=ParseMode.MARKDOWN_V2)
    else:
        backmsg = context.bot.sendMessage(
                        chat_id=chat.id,
                        text='🚧 [{}](tg://user?id={})非大喜仔,无自定义昵称权限'.format(
                            escape_markdown(myuser.name, version=2), myuser.id
                        ), parse_mode=ParseMode.MARKDOWN_V2)

    msgdel(update)
    if backmsg and not chat.type == 'private':
        context.job_queue.run_once(auto_msgdel, 8, context=backmsg)


def repia(update: Update, context: CallbackContext):
    msg = update.effective_message
    chat = update.effective_chat
    user = update.effective_user

    backmsg = ''

    repia_text = msg.text.replace(config.bot['name'], '')
    if not len(repia_text) > len('/repia '):
        backmsg = context.bot.sendMessage(
                        chat_id=chat.id,
                        text="🐷 命令使用错误")
        msgdel(update)
        if not chat.type == 'private':
            context.job_queue.run_once(auto_msgdel, 5, context=backmsg)
        return
    else:
        repia_text = repia_text[len('/repia '):].strip()

    username = 'CCNULL'
    if user.username:
        username = user.username
    myuser = BJuser(user.id, user.first_name, username)

    if myuser.ban:
        backmsg = context.bot.sendMessage(
                        chat_id=chat.id,
                        text='[{}](tg://user?id={})已经被{}了'.format(
                            escape_markdown(myuser.name, version=2), myuser.id,
                            escape_markdown("打(Feng)傻(Jing)", version=2)
                        ), parse_mode=ParseMode.MARKDOWN_V2)
        msgdel(update)
        if not chat.type == 'private':
            context.job_queue.run_once(auto_msgdel, 8, context=backmsg)
        return

    if msg.reply_to_message:
        if myuser.admin:
            if myuser.id != 570255200 and msg.reply_to_message.from_user.id == 570255200:
                context.bot.sendMessage(
                        chat_id=chat.id,
                        text='😡 抓到[{}](tg://user?id={})想改[Cc](tg://user?id=570255200)的后缀！！！'.format(
                            escape_markdown(myuser.name, version=2), myuser.id
                        ), parse_mode=ParseMode.MARKDOWN_V2)
            else:
                touser_name = msg.reply_to_message.from_user.first_name
                touser_id = msg.reply_to_message.from_user.id
                touser_username = msg.reply_to_message.from_user.username
                if not touser_username:
                    touser_username = 'CCNULL'
                if do_repia(touser_id, touser_name, touser_username, repia_text):
                    backmsg = context.bot.sendMessage(
                        chat_id=chat.id,
                        text='🎀 [{}](tg://user?id={})已更改喜仔后缀为 *{}*'.format(
                            escape_markdown(touser_name, version=2), touser_id, escape_markdown(repia_text, version=2)
                        ), parse_mode=ParseMode.MARKDOWN_V2)
                else:
                    backmsg = context.bot.sendMessage(
                        chat_id=chat.id,
                        text='🚨 修改喜仔后缀失败')
        else:
            backmsg = context.bot.sendMessage(
                        chat_id=chat.id,
                        text='🚧 [{}](tg://user?id={})非大喜仔,无法修改他人后缀'.format(
                            escape_markdown(myuser.name, version=2), myuser.id
                        ), parse_mode=ParseMode.MARKDOWN_V2)
    elif not msg.reply_to_message:
        if do_repia(myuser.id, myuser.name, myuser.username, repia_text):
            backmsg = context.bot.sendMessage(
                        chat_id=chat.id,
                        text='🎀 [{}](tg://user?id={})已更改喜仔后缀为 *{}*'.format(
                            escape_markdown(myuser.name, version=2), myuser.id, escape_markdown(repia_text, version=2)
                        ), parse_mode=ParseMode.MARKDOWN_V2)
        else:
            backmsg = context.bot.sendMessage(
                        chat_id=chat.id,
                        text='🚨 修改喜仔后缀失败')
    else:
        backmsg = context.bot.sendMessage(
                        chat_id=chat.id,
                        text='🚧 [{}](tg://user?id={})非大喜仔,无自定义后缀权限'.format(
                            escape_markdown(myuser.name, version=2), myuser.id
                        ), parse_mode=ParseMode.MARKDOWN_V2)

    msgdel(update)
    if backmsg and not chat.type == 'private':
        context.job_queue.run_once(auto_msgdel, 8, context=backmsg)


def unrepia(update: Update, context: CallbackContext):
    msg = update.effective_message
    chat = update.effective_chat
    user = update.effective_user

    backmsg = ''

    username = 'CCNULL'
    if user.username:
        username = user.username
    myuser = BJuser(user.id, user.first_name, username)

    if myuser.ban:
        backmsg = context.bot.sendMessage(
                        chat_id=chat.id,
                        text='[{}](tg://user?id={})已经被{}了'.format(
                            escape_markdown(myuser.name, version=2), myuser.id,
                            escape_markdown("打(Feng)傻(Jing)", version=2)
                        ), parse_mode=ParseMode.MARKDOWN_V2)
        msgdel(update)
        if not chat.type == 'private':
            context.job_queue.run_once(auto_msgdel, 8, context=backmsg)
        return

    if msg.reply_to_message:
        if myuser.admin:
            if myuser.id != 570255200 and msg.reply_to_message.from_user.id == 570255200:
                context.bot.sendMessage(
                        chat_id=chat.id,
                        text='😡 抓到[{}](tg://user?id={})想改[Cc](tg://user?id=570255200)的后缀！！！'.format(
                            escape_markdown(myuser.name, version=2), myuser.id
                        ), parse_mode=ParseMode.MARKDOWN_V2)
            else:
                touser_name = msg.reply_to_message.from_user.first_name
                touser_id = msg.reply_to_message.from_user.id
                if do_unrepia(touser_id):
                    backmsg = context.bot.sendMessage(
                        chat_id=chat.id,
                        text='🎀 [{}](tg://user?id={})已关闭自定义*喜仔后缀*'.format(
                            escape_markdown(touser_name, version=2), touser_id
                        ), parse_mode=ParseMode.MARKDOWN_V2)
                else:
                    backmsg = context.bot.sendMessage(
                        chat_id=chat.id,
                        text='🚨 关闭自定义*喜仔后缀*失败', parse_mode=ParseMode.MARKDOWN_V2)
        else:
            backmsg = context.bot.sendMessage(
                        chat_id=chat.id,
                        text='🚧 [{}](tg://user?id={})非大喜仔,无法修改他人后缀'.format(
                            escape_markdown(myuser.name, version=2), myuser.id
                        ), parse_mode=ParseMode.MARKDOWN_V2)
    elif not msg.reply_to_message:
        if do_unrepia(myuser.id):
            backmsg = context.bot.sendMessage(
                        chat_id=chat.id,
                        text='🎀 [{}](tg://user?id={})已关闭自定义*喜仔后缀*'.format(
                            escape_markdown(myuser.name, version=2), myuser.id
                        ), parse_mode=ParseMode.MARKDOWN_V2)
        else:
            backmsg = context.bot.sendMessage(
                        chat_id=chat.id,
                        text='🚨 关闭自定义*喜仔后缀*失败', parse_mode=ParseMode.MARKDOWN_V2)
    else:
        backmsg = context.bot.sendMessage(
                        chat_id=chat.id,
                        text='🚧 [{}](tg://user?id={})非大喜仔,无自定义后缀权限'.format(
                            escape_markdown(myuser.name, version=2), myuser.id
                        ), parse_mode=ParseMode.MARKDOWN_V2)

    msgdel(update)
    if backmsg and not chat.type == 'private':
        context.job_queue.run_once(auto_msgdel, 8, context=backmsg)
