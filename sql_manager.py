# coding:utf8
import sqlite3
import hashlib
import re
import random


class SQLManager(object):

    def __init__(self):
        pass

    @staticmethod
    def sql_connector(db_name="SQL_WEIBO.DB"):
        conn = sqlite3.connect(db_name)
        conn.text_factory = str
        return conn

    @staticmethod
    def sql_get_c(conn):
        return conn.cursor()

    def sql_get_cursor(self, db_name="SQL_WEIBO.DB"):
        conn = self.sql_connector(db_name)
        return self.sql_get_c(conn)

    @staticmethod
    def sql_commit_and_close(conn):
        conn.commit()
        conn.close()
        return True

    def make_table(self):
        conn = self.sql_connector()
        c = conn.cursor()
        c.execute("""CREATE TABLE USER (
        NO INTEGER PRIMARY KEY AUTOINCREMENT ,
        WEIBO_USER_ID VARCHAR(255) UNIQUE,
        GENDER VARCHAR(255),
        DESCRIPTION TEXT,
        BIRTHDAY VARCHAR(255),
        EDUCATION VARCHAR(255),
        ADDR TEXT,
        FOLLOW VARCHAR(255),
        WEIBO_CONTENT TEXT,
        IS_ACTIVE INT,
        MORE_INFO TEXT,
        IS_USED INT,
        AVATAR_URL TEXT,
        IS_BIG_V INT,
        IS_VIP INT,
        NICKNAME VARCHAR(255),
        TOTAL_WEIBO INT,
        VARIFY TEXT,
        ALL_REPO INT,
        FANS_TOTAL INT,
        FOLLOW_TOTAL INT,
        MINE_FINISHED INT,
        CLOSE_FANS INT
    )
    """)
        # conn.commit()
        # conn.close()
        self.sql_commit_and_close(conn)
        return True

    def flag_user_finished(self, weibo_user_id):
        conn = self.sql_connector()
        c = conn.cursor()
        c.execute("""UPDATE USER SET MINE_FINISHED = 1 WHERE WEIBO_USER_ID=?""", (weibo_user_id, ))
        self.sql_commit_and_close(conn)
        return

    def get_user_fans_list(self, weibo_user_id, split_sign='&;', tasksheet='task_sheet.txt'):
        conn = self.sql_connector()
        c = conn.cursor()
        res = c.execute("""SELECT FOLLOW FROM USER WHERE WEIBO_USER_ID=?""", (weibo_user_id,))
        work_li = None
        for item in res:
            work_li = str(item[0]).split(split_sign)
            break
        s = ''
        print(work_li)
        for item in work_li:
            s += item + '\n'
        with open(tasksheet, 'wb') as f:
            f.write(s)
            f.close()
        return len(work_li)

    def instance_new_user(self, WEIBO_USER_ID,
                          GENDER,
                          DESCRIPTION,
                          BIRTHDAY,
                          EDUCATION,
                          ADDR,
                          FOLLOW,
                          WEIBO_CONTENT,
                          IS_ACTIVE,
                          IS_BIG_V,
                          NICKNAME,
                          TOTAL_WEIBO,
                          VARIFY, ALL_REPO, FANS_TOTAL, FOLLOW_TOTAL, CLOSE_FANS, AVATAR_URL, IS_USED=0):
        conn = self.sql_connector()
        c = conn.cursor()
        try:
            c.execute("""INSERT INTO USER (WEIBO_USER_ID, GENDER, DESCRIPTION, BIRTHDAY, EDUCATION, ADDR, FOLLOW, WEIBO_CONTENT, IS_ACTIVE, IS_USED, IS_BIG_V, NICKNAME, TOTAL_WEIBO, VARIFY, ALL_REPO, FANS_TOTAL, FOLLOW_TOTAL, MINE_FINISHED, CLOSE_FANS, AVATAR_URL) VALUES 
(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0, ?, ?)""", (WEIBO_USER_ID,
                          GENDER,
                          DESCRIPTION,
                          BIRTHDAY,
                          EDUCATION,
                          ADDR,
                          FOLLOW,
                          WEIBO_CONTENT,
                          IS_ACTIVE,
                          IS_USED,
                          IS_BIG_V,
                          NICKNAME,
                          TOTAL_WEIBO,
                          VARIFY,
                          ALL_REPO,
                          FANS_TOTAL,
                          FOLLOW_TOTAL,
                          CLOSE_FANS,
                          AVATAR_URL))
        except :
            print("there's a question occured.")
        self.sql_commit_and_close(conn)
        return


    def is_user_exist(self, weibo_id):
        conn = self.sql_connector()
        c = conn.cursor()
        res = c.execute("SELECT * FROM USER WHERE WEIBO_USER_ID=?", (weibo_id,))
        for _ in res:
            return True
        return False

    def select_a_user_not_use(self, r=True):
        conn = self.sql_connector()
        c = conn.cursor()
        res = c.execute("""SELECT WEIBO_USER_ID FROM USER WHERE IS_USED=0""")
        if res:
            li = [item for item in res]
            random.shuffle(li)
            for item in li:
                return item
        return False

    def flag_user_used(self, USER_WEIBO_ID):
        conn = self.sql_connector()
        c = conn.cursor()
        c.execute("""UPDATE USER SET IS_USED=1 WHERE WEIBO_USER_ID=?""", (USER_WEIBO_ID, ))
        self.sql_commit_and_close(conn)
        return True

if __name__ == '__main__':

    sql_m = SQLManager()
    # sql_m.make_table()
    conn = sql_m.sql_connector()
    #
    c = conn.cursor()

    # c.execute("""UPDATE USER SET IS_USED=0 WHERE FOLLOW=?""",
    #           ('2425540891&;2286081102&;2425540891&;5686095920&;2425540891&;5686095920',))
    # for i in range(2, 10, 1):
    #     c.execute("""DELETE FROM USER WHERE NO = ?""", (i, ))
    # sql_m.sql_commit_and_close(conn)
    res = c.execute("""SELECT count(*) FROM USER""")
    for item in res:
        print(item)











