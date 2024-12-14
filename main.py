import config

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters, CallbackQueryHandler

from mode_admin.group import group_set, set_callback
from mode_data.write_txt import nowtime
from mode_fun.warm import warm, warmrank, warmrankclear
from mode_fun.edit import rename, unrename, repia, unrepia
from mode_admin.Cc import ccadd, ccdel, setpia, ccban, ccunban, cc_pro
from mode_fun.msgdel import msgdel, keyboard_msgdel, auto_msgdel, all_comdel
from mode_user.user import check_info

Main_Bot = config.bot['key']
Bot_Name = config.bot['name']
REQUEST_KWARGS = {
    'proxy_url': config.proxy
}

tgbot = Updater(Main_Bot, request_kwargs=REQUEST_KWARGS)


def start(update: Update, context: CallbackContext):
    update.message.reply_text('🚨 CC代码写得很烂！')
    msgdel(update)


def cc(update: Update, context: CallbackContext):
    chat = update.effective_chat
    thetime = nowtime()
    backmsg = context.bot.sendMessage(
                        chat_id=chat.id,
                        text="中国时间：\n{}\nBot服务器时间：\n{}\n\n当前代码版本号：V{}\n\n😎喜仔我还活着哦~~~".format(
                            thetime[0], thetime[1], config.Version
                        ))
    msgdel(update)
    if backmsg and not update.message.chat.type == 'private':
        context.job_queue.run_once(auto_msgdel, 5, context=backmsg)


def callback_query(update: Update, context: CallbackContext) -> None:
    # print(context.dispatcher)
    print(update.callback_query.chat_instance)


def cb_return(update: Update, context: CallbackContext) -> None:
    update.callback_query.answer()
    keyboard_msgdel(update)


def main() -> None:
    """Start the bot."""
    dispatcher = tgbot.dispatcher

    # 一般用户
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("cc", cc))
    dispatcher.add_handler(CommandHandler("warm", warm))

    # 普通管理员
    dispatcher.add_handler(CommandHandler("wrank", warmrank))
    dispatcher.add_handler(CommandHandler("wclear", warmrankclear))
    dispatcher.add_handler(CommandHandler("xzset", group_set))

    # BOT管理员
    dispatcher.add_handler(CommandHandler("rename", rename))
    dispatcher.add_handler(CommandHandler("unrename", unrename))
    dispatcher.add_handler(CommandHandler("repia", repia))
    dispatcher.add_handler(CommandHandler("unrepia", unrepia))
    dispatcher.add_handler(CommandHandler("xzinfo", check_info))

    # 超级管理员
    dispatcher.add_handler(CommandHandler("ccadd", ccadd))
    dispatcher.add_handler(CommandHandler("ccdel", ccdel))
    dispatcher.add_handler(CommandHandler("setpia", setpia))
    dispatcher.add_handler(CommandHandler("hot", ccban))
    dispatcher.add_handler(CommandHandler("unhot", ccunban))

    # dispatcher.add_handler(MessageHandler(Filters.regex(r'^66'), text))
    dispatcher.add_handler(MessageHandler(Filters.chat(chat_id=570255200), cc_pro))
    dispatcher.add_handler(MessageHandler(Filters.command, all_comdel))

    # 回调函数
    dispatcher.add_handler(CallbackQueryHandler(cb_return, pattern='back'))
    dispatcher.add_handler(CallbackQueryHandler(callback_query, pattern='test'))

    dispatcher.add_handler(CallbackQueryHandler(set_callback, pattern='group_set_null'))
    dispatcher.add_handler(CallbackQueryHandler(set_callback, pattern='group_set_back'))
    dispatcher.add_handler(CallbackQueryHandler(set_callback, pattern='group_set_del_chat'))
    dispatcher.add_handler(CallbackQueryHandler(set_callback, pattern='group_set_del_com'))
    dispatcher.add_handler(CallbackQueryHandler(set_callback, pattern='group_set_del_allcom'))

    # error
    # dispatcher.add_error_handler(error)

    # 定时执行
    # tgbot.job_queue.run_repeating(test, interval=5, first=0)

    # 启动机器人，勿删
    tgbot.start_polling()
    tgbot.bot.sendMessage(570255200, "服务已上线")
    tgbot.idle()


if __name__ == '__main__':
    main()
