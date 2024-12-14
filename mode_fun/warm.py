from telegram import Update, ParseMode
from telegram.ext import CallbackContext
from telegram.utils.helpers import escape_markdown

from mode_user.user import BJuser, build_user
from mode_data.database import warm_add, get_rank, do_rankclear
from mode_fun.msgdel import msgdel, auto_msgdel


def warm(update: Update, context: CallbackContext):
    msg = update.effective_message
    chat = update.effective_chat

    myuser = build_user(update)

    user_name = myuser.name
    if myuser.rename:
        user_name = myuser.rename_text

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

    if chat.type == 'private':
        context.bot.sendMessage(
                        chat_id=chat.id,
                        text='*你为什么要偷偷给自己大逼兜*', parse_mode=ParseMode.MARKDOWN_V2)
    else:
        if msg.reply_to_message:
            touser_name = msg.reply_to_message.from_user.first_name
            touser_id = msg.reply_to_message.from_user.id
            touser_username = msg.reply_to_message.from_user.username

            reuser = BJuser(touser_id, touser_name, touser_username)
            if reuser.rename:
                touser_name = reuser.rename_text

            if myuser.pia == -1:
                context.bot.sendMessage(
                        chat_id=chat.id,
                        text='[{}](tg://user?id={})给了[{}](tg://user?id={}){}'.format(
                            escape_markdown(user_name, version=2), myuser.id,
                            escape_markdown(touser_name, version=2), touser_id,
                            escape_markdown(myuser.pia_text, version=2)
                        ), parse_mode=ParseMode.MARKDOWN_V2)
            else:
                context.bot.sendMessage(
                        chat_id=chat.id,
                        text='[{}](tg://user?id={})给了[{}](tg://user?id={})一个大逼兜✋'.format(
                            escape_markdown(user_name, version=2), myuser.id,
                            escape_markdown(touser_name, version=2), touser_id
                        ), parse_mode=ParseMode.MARKDOWN_V2)

            warm_add(chat.id, chat.title, myuser.id, myuser.name, 'attack', myuser.pia_num)
            warm_add(chat.id, chat.title, reuser.id, reuser.name, 'attacked', myuser.pia_num)

        else:
            if myuser.pia == -1:
                context.bot.sendMessage(
                        chat_id=chat.id,
                        text='[{}](tg://user?id={})给了自己{}'.format(
                            escape_markdown(user_name, version=2), myuser.id,
                            escape_markdown(myuser.pia_text, version=2)
                        ),
                        parse_mode=ParseMode.MARKDOWN_V2)
            else:
                context.bot.sendMessage(
                        chat_id=chat.id,
                        text='[{}](tg://user?id={})给了自己一个大逼兜✋'.format(
                            escape_markdown(user_name, version=2), myuser.id,
                        ), parse_mode=ParseMode.MARKDOWN_V2)
            warm_add(chat.id, chat.title, myuser.id, myuser.name, 'attack', myuser.pia_num)
            warm_add(chat.id, chat.title, myuser.id, myuser.name, 'attacked', myuser.pia_num)

    msgdel(update)


def warmrank(update: Update, context: CallbackContext):
    chat = update.effective_chat
    user = update.effective_user

    autodel_mode = 0
    backmsg = ''

    username = 'CCNULL'
    if user.username:
        username = user.username
    myuser = BJuser(user.id, user.first_name, username)

    if chat.type == 'private':
        context.bot.sendMessage(
                        chat_id=chat.id,
                        text='🏅 众所周知，你吃的大逼兜最多')
    else:
        check_admin = myuser.admin

        if not check_admin:
            check_admin = myuser.groupadmin(chat.id)

        if check_admin:
            rank_text = "*大逼兜排行榜：*\n"
            attack = get_rank(chat.id, 'attack')
            attacked = get_rank(chat.id, 'attacked')

            rank_text = rank_text + "\n进攻阵营:\n"

            # jiangpai = ['🥇', '🥈', '🥉', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']

            for i in range(len(attack)):
                rank_text = rank_text + "{} [{}](tg://user?id={}) 👉 {} \n".format(
                    # jiangpai[i],
                    '😈',
                    escape_markdown(attack[i][3], version=2), attack[i][2],
                    escape_markdown(str(attack[i][4]), version=2)
                )

            rank_text = rank_text + "\n受击阵营:\n"

            for i in range(len(attacked)):
                rank_text = rank_text + "{} [{}](tg://user?id={}) 👉 {} \n".format(
                    # jiangpai[i],
                    '🥺',
                    escape_markdown(attacked[i][3], version=2), attacked[i][2],
                    escape_markdown(str(attacked[i][5]), version=2)
                )

            backmsg = context.bot.sendMessage(
                        chat_id=chat.id,
                        text=rank_text, parse_mode=ParseMode.MARKDOWN_V2)
            autodel_mode = 1
        else:
            backmsg = context.bot.sendMessage(
                        chat_id=chat.id,
                        text='🏅 [{}](tg://user?id={})是吃大逼兜专业户'.format(
                            escape_markdown(myuser.name, version=2), myuser.id
                        ), parse_mode=ParseMode.MARKDOWN_V2)
            autodel_mode = 2

    msgdel(update)
    if autodel_mode and backmsg and not chat.type == 'private':
        if autodel_mode == 1:
            context.job_queue.run_once(auto_msgdel, 10, context=backmsg)
        else:
            context.job_queue.run_once(auto_msgdel, 5, context=backmsg)


def warmrankclear(update: Update, context: CallbackContext):
    chat = update.effective_chat
    user = update.effective_user
    backmsg = ''

    username = 'CCNULL'
    if user.username:
        username = user.username
    myuser = BJuser(user.id, user.first_name, username)

    if not chat.type == 'private':
        if myuser.id == 570255200 or myuser.groupadmin(chat.id):
            num = do_rankclear(chat.id)
            if num == -1:
                backmsg = context.bot.sendMessage(
                        chat_id=chat.id,
                        text="❌ 重置该群组排行榜失败")
            else:
                context.bot.sendMessage(
                        chat_id=chat.id,
                        text="♻ 本群的{}位用户记录已重置".format(num))
        else:
            backmsg = context.bot.sendMessage(
                        chat_id=chat.id,
                        text='🚧 无权限重置排行榜，[{}](tg://user?id={})不是群组管理员'.format(
                            escape_markdown(myuser.name, version=2), myuser.id
                        ), parse_mode=ParseMode.MARKDOWN_V2)
    msgdel(update)
    if backmsg and not chat.type == 'private':
        context.job_queue.run_once(auto_msgdel, 5, context=backmsg)


if __name__ == '__main__':
    # add(0, '1', 0, '1', 'attacked', 1)
    get_rank(-1001518926694, 'attacked')
