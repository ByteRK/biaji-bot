import pymysql
import config


def set_conn(db='tgbot_biaji') -> pymysql.Connection:
    conn = pymysql.connect(
        host=config.datebase['host'], port=config.datebase['port'],
        user=config.datebase['user'], password=config.datebase['password'],
        database=db, charset=config.datebase['charset'],
    )
    return conn


def group_seach(group_id, group_name) -> any:
    del_com = 1
    del_chat = 1
    del_allcom = 0

    conn = set_conn()
    cursor = conn.cursor()
    sql = "SELECT `del_com`,`del_chat`,`del_allcom`" \
          "FROM `group` WHERE group_id={}".format(group_id)
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        # print(results)
        if results:
            del_com = results[0][0]
            del_chat = results[0][1]
            del_allcom = results[0][2]
        else:
            group_add(group_id, group_name)
    except Exception as e:
        print('读取群组信息错误')
        conn.rollback()
        print(repr(e))
    conn.close()
    return del_com, del_chat, del_allcom


def group_set(group_id, mode, value):
    conn = set_conn()
    cursor = conn.cursor()

    sql = "UPDATE `group` SET {}={} WHERE group_id={}".format(
        mode, value, group_id
    )

    try:
        cursor.execute(sql)
        conn.commit()
    except Exception as e:
        print('写入用户信息错误')
        conn.rollback()
        print(repr(e))
        return False
    return True


def group_add(group_id, group_name):
    conn = set_conn()
    cursor = conn.cursor()
    sql = "INSERT INTO `group` (`group_id`,`group_name`,`del_com`,`del_chat`,`del_allcom`) " \
          "VALUES ({},'{}','{}',{},{})".format(group_id, group_name, 1, 1, 0)
    try:
        cursor.execute(sql)
        conn.commit()
    except Exception as e:
        print('写入用户信息错误')
        conn.rollback()
        print(repr(e))
        return False
    return True


def user_seach(user_id, name, username) -> any:
    # print(str(user_id) + '-' + name + '-' + username)
    pia = 1
    pia_text = ''
    pia_num = 1
    rename = 0
    rename_text = ''
    admin = 0
    ban = 0
    ban_text = ''
    ban_admin = ''

    conn = set_conn()
    cursor = conn.cursor()
    sql = "SELECT `pia`,`pia_text`,`pia_num`,`rename`,`rename_text`,`admin`,`ban`,`ban_text`,`ban_admin` " \
          "FROM user WHERE id={}".format(user_id)
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        # print(results)
        if results:
            pia = results[0][0]
            pia_text = results[0][1]
            pia_num = results[0][2]
            rename = results[0][3]
            rename_text = results[0][4]
            admin = results[0][5]
            ban = results[0][6]
            ban_text = results[0][7]
            ban_admin = results[0][8]
        else:
            user_add(user_id, name, username)
    except Exception as e:
        print('读取用户信息错误')
        conn.rollback()
        print(repr(e))
    conn.close()
    return pia, pia_text, pia_num, rename, rename_text, admin, ban, ban_text, ban_admin


def user_add(user_id, name, username) -> bool:
    conn = set_conn()
    cursor = conn.cursor()
    sql = "INSERT INTO user (`id`,`name`,`username`,`pia`,`pia_num`,`rename`,`admin`,`ban`) " \
          "VALUES ({},'{}','{}',{},{},{},{},{})".format(user_id, name, username, 1, 1, 0, 0, 0)
    try:
        cursor.execute(sql)
        conn.commit()
    except Exception as e:
        print('写入用户信息错误')
        conn.rollback()
        print(repr(e))
        return False
    return True


def warm_add(group_id, group_name, user_id, user_name, state, num) -> None:
    conn = set_conn()
    cursor = conn.cursor()
    sql = "SELECT {} FROM warm WHERE group_id={} and user_id={}".format(
        state, group_id, user_id
    )
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        if results:
            num = num + results[0][0]
            # print(results[0][0])
            sql = "UPDATE warm SET group_name='{}',user_name='{}',{}={} WHERE group_id={} and user_id={}".format(
                group_name, user_name, state, num, group_id, user_id
            )
            try:
                cursor.execute(sql)
                conn.commit()
            except Exception as e:
                # print('1')
                conn.rollback()
                print(repr(e))
        else:
            attack = attacked = 0
            if state == 'attack':
                attack = num
            else:
                # print(group_id, group_name, user_id, user_name)
                attacked = num
            sql = "INSERT INTO warm (`group_id`, `group_name`, `user_id`, `user_name`, `attack`, `attacked`) VALUES" \
                  " ({}, '{}', {}, '{}', {}, {} )".format(group_id, group_name, user_id, user_name, attack, attacked)
            try:
                cursor.execute(sql)
                conn.commit()
            except Exception as e:
                conn.rollback()
                print(repr(e))
    except Exception as e:
        conn.rollback()
        print(repr(e))
    conn.close()


def get_rank(group_id, state, num=5) -> list:
    output = []
    conn = set_conn()
    cursor = conn.cursor()
    sql = "SELECT * FROM warm WHERE group_id={} ORDER BY {} desc".format(group_id, state)
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for i in range(len(results)):
            if i == num:
                break
            output.append(results[i])
    except Exception as e:
        conn.rollback()
        print(repr(e))
    conn.close()
    return output


def do_rename(user_id, name, username, rename_text) -> bool:
    conn = set_conn()
    cursor = conn.cursor()
    results = 0
    sql = "UPDATE user SET `rename`=1,`rename_text`='{}' WHERE `id`={}".format(rename_text, user_id)
    try:
        results = cursor.execute(sql)
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(repr(e))
    if not results:
        if user_add(user_id, name, username):
            do_rename(user_id, name, username, rename_text)
            return True
        else:
            return False
    conn.close()
    return True


def do_unrename(user_id) -> bool:
    conn = set_conn()
    cursor = conn.cursor()
    results = 0
    sql = "UPDATE user SET `rename`=0 WHERE `id`={}".format(user_id)
    try:
        results = cursor.execute(sql)
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(repr(e))
    conn.close()
    if not results:
        return False
    return True


def do_repia(user_id, name, username, repia_text) -> bool:
    conn = set_conn()
    cursor = conn.cursor()
    results = 0
    sql = "UPDATE user SET `pia`=-1,`pia_text`='{}' WHERE `id`={}".format(repia_text, user_id)
    try:
        results = cursor.execute(sql)
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(repr(e))
    if not results:
        if user_add(user_id, name, username):
            do_repia(user_id, name, username, repia_text)
            return True
        else:
            return False
    conn.close()
    return True


def do_unrepia(user_id) -> bool:
    conn = set_conn()
    cursor = conn.cursor()
    results = 0
    sql = "UPDATE user SET `pia`=1 WHERE `id`={}".format(user_id)
    try:
        results = cursor.execute(sql)
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(repr(e))
    conn.close()
    if not results:
        return False
    return True


def do_rankclear(group_id) -> int:
    conn = set_conn()
    cursor = conn.cursor()
    sql = "DELETE FROM warm WHERE group_id='{}'".format(group_id)
    try:
        cursor.execute(sql)
        results = cursor.rowcount
        conn.commit()
    except Exception as e:
        conn.rollback()
        results = -1
        print(repr(e))
    conn.close()
    return results
