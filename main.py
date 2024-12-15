import config

from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext, MessageHandler, filters, CallbackQueryHandler

from mode_admin.group import group_set, set_callback
from mode_data.write_txt import nowtime
from mode_fun.warm import warm, warmrank, warmrankclear
from mode_fun.edit import rename, unrename, repia, unrepia
from mode_admin.author import ccadd, ccdel, setpia, ccban, ccunban, cc_pro
from mode_fun.msgdel import msgdel, keyboard_msgdel, auto_msgdel, all_comdel
from mode_user.user import check_info

Main_Bot = config.bot['key']
Bot_Name = config.bot['name']

async def start(update: Update, context: CallbackContext):
    await context.bot.send_message(update.effective_chat.id,'🚨 CC代码写得很烂！')
    await msgdel(update, context)


async def cc(update: Update, context: CallbackContext):
    chat = update.effective_chat
    thetime = nowtime()
    backmsg = await context.bot.sendMessage(
                        chat_id=chat.id,
                        text="中国时间：\n{}\nBot服务器时间：\n{}\n\n当前代码版本号：V{}\n\n😎喜仔我还活着哦~~~".format(
                            thetime[0], thetime[1], config.Version
                        ))
    await msgdel(update, context)
    if backmsg and not update.message.chat.type == 'private':
        context.job_queue.run_once(auto_msgdel, 5, data={
            'bot': context.bot,
            'chat':backmsg.chat,
            'message_id': backmsg.message_id
        })


def callback_query(update: Update, context: CallbackContext) -> None:
    # print(context.dispatcher)
    print(update.callback_query.chat_instance)


async def cb_return(update: Update, context: CallbackContext) -> None:
    await update.callback_query.answer()
    await keyboard_msgdel(update, context)


def main() -> None:
    """Start the bot."""

    application = Application.builder().token(Main_Bot).build()
    application.add_handler(CommandHandler("start", start))

    # 一般用户
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("cc", cc))
    application.add_handler(CommandHandler("warm", warm))

    # 普通管理员
    application.add_handler(CommandHandler("wrank", warmrank))
    application.add_handler(CommandHandler("wclear", warmrankclear))
    application.add_handler(CommandHandler("xzset", group_set))

    # BOT管理员
    application.add_handler(CommandHandler("rename", rename))
    application.add_handler(CommandHandler("unrename", unrename))
    application.add_handler(CommandHandler("repia", repia))
    application.add_handler(CommandHandler("unrepia", unrepia))
    application.add_handler(CommandHandler("xzinfo", check_info))

    # 超级管理员
    application.add_handler(CommandHandler("ccadd", ccadd))
    application.add_handler(CommandHandler("ccdel", ccdel))
    application.add_handler(CommandHandler("setpia", setpia))
    application.add_handler(CommandHandler("hot", ccban))
    application.add_handler(CommandHandler("unhot", ccunban))

    # application.add_handler(MessageHandler(filters.regex(r'^66'), text))
    # application.add_handler(MessageHandler(filters.chat(chat_id=config.author), cc_pro))
    # application.add_handler(MessageHandler(filters.command, all_comdel))

    # 回调函数
    application.add_handler(CallbackQueryHandler(cb_return, pattern='back'))
    application.add_handler(CallbackQueryHandler(callback_query, pattern='test'))

    application.add_handler(CallbackQueryHandler(set_callback, pattern='group_set_null'))
    application.add_handler(CallbackQueryHandler(set_callback, pattern='group_set_back'))
    application.add_handler(CallbackQueryHandler(set_callback, pattern='group_set_del_chat'))
    application.add_handler(CallbackQueryHandler(set_callback, pattern='group_set_del_com'))
    application.add_handler(CallbackQueryHandler(set_callback, pattern='group_set_del_allcom'))

    # error
    # dispatcher.add_error_handler(error)

    # 启动机器人，勿删
    application.run_polling()


if __name__ == '__main__':
    main()
