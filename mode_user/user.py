from telegram import Update
from telegram.ext import CallbackContext

import config
from mode_admin.admin import checkgroupadmin, checkgroup
from mode_data.database import user_seach
from mode_fun.msgdel import auto_msgdel, msgdel


class BJuser:
    def __init__(self, user_id, name, username):
        self.id = user_id
        self.name = name
        self.username = username
        data = user_seach(user_id, name, username)
        self.pia = data[0]
        self.pia_text = data[1]
        self.pia_num = data[2]
        self.rename = data[3]
        self.rename_text = data[4]
        self.admin = data[5]
        self.ban = data[6]
        self.ban_text = data[7]
        self.ban_admin = data[8]

    def getinfo(self):
        return self.id, self.name, self.username

    def groupadmin(self, group_id) -> bool:
        return checkgroupadmin(self.id, group_id)

    def ingroup(self, group_id) -> bool:
        return checkgroup(self.id, group_id)


def build_user(update: Update) -> BJuser:
    user = update.effective_user

    username = 'CCNULL'
    if user.username:
        username = user.username
    myuser = BJuser(user.id, user.first_name, username)
    return myuser


async def check_info(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    msg = update.effective_message
    username = 'CCNULL'
    if user.username:
        username = user.username
    myuser = BJuser(user.id, user.first_name, username)

    if myuser.admin:
        returnmsg = '👀 喜仔信息查询:\n\n'

        if msg.reply_to_message:
            touser_name = msg.reply_to_message.from_user.first_name
            touser_id = msg.reply_to_message.from_user.id
            touser_username = 'CCNULL'
            if msg.reply_to_message.from_user.username:
                touser_username = msg.reply_to_message.from_user.username
            myuser = BJuser(touser_id, touser_name, touser_username)

        returnmsg += '姓名: {}\n'.format(str(myuser.name))
        returnmsg += 'TGID: {}\n'.format(str(myuser.id))
        if myuser.username != 'CCNULL':
            returnmsg += '用户名: @{}\n'.format(myuser.username)
        if myuser.rename:
            returnmsg += '自定义昵称: {}\n'.format(myuser.rename_text)
        if myuser.pia:
            returnmsg += '自定义后缀: {}\n'.format(myuser.pia_text)
        returnmsg += '大逼兜权重: {}\n'.format(myuser.pia_num)
        returnmsg += '是否大喜仔: {}\n'.format(str(myuser.admin).replace('1', '是').replace('0', '否'))
        if myuser.ban:
            returnmsg += '是否被封禁: 是\n封禁者: {}\n封禁原因: {}'.format(
                myuser.ban_admin.replace(str(config.author), '大喜仔Cc'), myuser.ban_text
            )

        backmsg = await context.bot.sendMessage(
                        chat_id=update.effective_chat.id,
                        text=returnmsg)
        await msgdel(update, context)
        context.job_queue.run_once(auto_msgdel, 8, data={
            'bot': context.bot,
            'chat':backmsg.chat,
            'message_id': backmsg.message_id
        })


if __name__ == '__main__':
    a = BJuser(10, 'kk', 'kk')
    print(a.username)
