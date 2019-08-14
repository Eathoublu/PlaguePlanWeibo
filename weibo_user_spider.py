# coding:utf8
import requests
import re
from time import sleep
import hashlib
from sql_manager import SQLManager
from parser import WeiboContentParser, UserFansParser, UserInfoParser, UserCCParser, UserFansParserV2
from time import sleep
from tqdm import tqdm
from random import random

class UserSpider(object):

    def __init__(self, enterance='https://weibo.cn/6654487920/fans'):
        # cookie = '_T_WM=68703098422; ALF=1567576090; SCF=Aj-0lsYi_X9L5GCwSl9hebeeMjNSUDesgki_L1puzuN3iV98rSIi_emOUe51OhD3ie01P329IxZ1klQXvAi17ZI.; SUB=_2A25wQ7NKDeRhGeNH7VQY-C_OzD6IHXVTz90CrDV6PUNbktAKLUXGkW1NSoE5VJ_wBwkDwrSHYHXdADLTvyMp7vlD; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9Wh1R.LrD0R2g_vOjx-2RlOs5JpX5KMhUgL.Fo-4Soq41h2ES0z2dJLoI7yDdPWEdN9LSBtt; SUHB=0G0e0uICryEado; SSOLoginState=1564984091; _T_WL=1; _WEIBO_UID=5966981272; MLOGIN=1; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D1076031737263204'
        self.cookie = '_WEIBO_UID=5966981272; _T_WM=62902696990; ALF=1568366628; SCF=Aj-0lsYi_X9L5GCwSl9hebeeMjNSUDesgki_L1puzuN3Sa5Vf7pBYfbnSQHxxaiJNapj6tyRXL0BPp52mdW4tMs.; SUB=_2A25wV6OVDeRhGeNH7VQY-C_OzD6IHXVTu83drDV6PUJbktAKLRPCkW1NSoE5VJpfn0cZiTXSXoGGdQNi0BDw7dEM; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9Wh1R.LrD0R2g_vOjx-2RlOs5JpX5K-hUgL.Fo-4Soq41h2ES0z2dJLoI7yDdPWEdN9LSBtt; SUHB=0ftZqBOyubXqAQ; SSOLoginState=1565774789'
        self.cookie_dict = {i.split("=")[0]: i.split("=")[-1] for i in self.cookie.split("; ")}
        self.headers = {
            ':authority': 'weibo.cn',
            ':method': 'GET',
            ':path': '/1737263204/fans',
            ':scheme': 'https',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'referer': 'https://weibo.cn/u/1737263204',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
        }
        self.fans_headers = {
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
        }
        self.s = requests.session()
        self.sql_manager = SQLManager()
        self.weibo_content_parser = WeiboContentParser
        self.user_info_parser = UserInfoParser
        self.user_fans_parser = UserFansParserV2
        self.user_cc_parser = UserCCParser

    def request(self, url, fans=False):
        sleep(random()*5)
        if fans:
            req = self.s.get(url=url, headers=self.fans_headers)
        else:
            req = self.s.get(url, headers=self.headers, cookies=self.cookie_dict)
        return req.content

    # @staticmethod
    # def get_fans_list(fans_content):
    #     r = re.compile('[0-9]{10}', re.S)
    #     fans_li = r.findall(fans_content)
    #     return fans_li

    # @staticmethod
    # def get_user_weibo_content(split_sign='&;//***//***//***&;'):
    #
    #     return user_weibo_content

    def get_next_request_user_id(self):
        next_user_id = self.sql_manager.select_a_user_not_use()
        return next_user_id

    # def request_this_user(self, user_weibo_id):
    #     self.sql_manager.flag_user_used(user_weibo_id)

    def is_valid_request(self, content):
        pass
        return True

    def set_cookie(self, cookie_string):
        self.cookie = cookie_string
        self.cookie_dict = {i.split("=")[0]: i.split("=")[-1] for i in self.cookie.split("; ")}


    @staticmethod
    def string_factory(s):
        # try:
        #     return s.encode('raw_unicode_escape')
        # except:
        #     return s
        return s

    def run(self):

        while True:
            try:
                get_a_new_user = self.get_next_request_user_id()
                if not get_a_new_user:
                    print('[Finished]now quit.')
                    # break

                # print(get_a_new_user)
                get_a_new_user = get_a_new_user[0]
                self.sql_manager.get_user_fans_list(get_a_new_user)
                self.sql_manager.flag_user_used(get_a_new_user)
                with open('task_sheet.txt') as tf:
                    now_request_user = tf.readline()
                    while now_request_user[:-1]:
                        try:
                            sleep(0.3)
                            print('[info]now next user, user id {}'.format(now_request_user[:-1]))
                            if self.sql_manager.is_user_exist(now_request_user[:-1]):
                                print('[Info]Get a re-request user,pass.')
                                now_request_user = tf.readline()
                                continue
                            weibo_user_id = now_request_user[:-1]
                            url_profile = 'https://weibo.cn/' + weibo_user_id + '/profile'
                            # url_fans = 'https://weibo.cn/' + weibo_user_id + '/fans'
                            url_fans = 'https://m.weibo.cn/api/container/getIndex?containerid=231051_-_fans_-_'+ weibo_user_id +'&since_id=1'
                            url_info = 'https://weibo.cn/' + weibo_user_id + '/info'
                            profile_content = self.request(url=url_profile)
                            fans_content_page_1 = self.request(url=url_fans, fans=True)
                            info_content = self.request(url=url_info)
                            if self.is_valid_request(content=profile_content) and self.is_valid_request(info_content):
                                wcp = self.weibo_content_parser(weibo_content=profile_content)
                                weibo_total, follow_total, fans_total = wcp.get_total()
                                weibo_content_string, all_repo = wcp.get_weibo_content_to_string_and_all_repo()
                                # weibo_cc_url_string = wcp.get_cc_url_li_to_string()
                                weibo_cc_url_li = wcp.get_cc_url()
                                c_f = ''
                                for u in tqdm(weibo_cc_url_li):
                                    cc_content = self.request(u)
                                    ucp = self.user_cc_parser(cc_content=cc_content, weibo_user_id=weibo_user_id)
                                    c_f += ucp.get_close_fans_to_string()
                                uip = self.user_info_parser(user_info_content=info_content)
                                avatar_url, nickname, gender, addr, birthday, is_vip, description, education, varify = uip.get_user_info()
                                ufp = self.user_fans_parser(fans_content=fans_content_page_1)
                                fans_s = ''
                                fans_s += ufp.get_fans_list_to_string()
                                fans_page = 1
                                status = ufp.get_status()
                                while status == 1:
                                    fans_page += 1
                                    print('[info]now scanning page {} of fans.'.format(str(fans_page)))
                                    next_fans_url = 'https://m.weibo.cn/api/container/getIndex?containerid=231051_-_fans_-_'+ weibo_user_id +'&since_id=' + str(fans_page)
                                    fans_content = self.request(next_fans_url, fans=True)
                                    ufp_p = self.user_fans_parser(fans_content=fans_content)
                                    fans_s += ufp_p.get_fans_list_to_string()
                                    status = ufp_p.get_status()
                                # total_page = ufp.get_page_amount()
                                # print('[info]fans page:', total_page)
                                # fans_s = ''
                                # fans_s += ufp.get_fans_list_to_string()
                                # if total_page != 1:
                                    # for page in tqdm(range(2, int(total_page)+2)):
                                    #     sleep(0.3)
                                    #     fans_page_url = 'https://weibo.cn/' + weibo_user_id + '/fans?page='+str(page)
                                    #     fans_page_content = self.request(url=fans_page_url)
                                    #     ufp_p = self.user_fans_parser(fans_contant=fans_page_content)
                                    #     fans_s += ufp_p.get_fans_list_to_string()

                                self.sql_manager.instance_new_user(WEIBO_USER_ID=weibo_user_id,
                                                                   GENDER=self.string_factory(gender),
                                                                   DESCRIPTION=self.string_factory(education),
                                                                   BIRTHDAY=birthday,
                                                                   EDUCATION=self.string_factory(education),
                                                                   ADDR=self.string_factory(addr),
                                                                   FOLLOW=fans_s,
                                                                   WEIBO_CONTENT=self.string_factory(weibo_content_string),
                                                                   IS_ACTIVE=None,
                                                                   IS_BIG_V=is_vip,
                                                                   NICKNAME=self.string_factory(nickname),
                                                                   TOTAL_WEIBO=weibo_total,
                                                                   VARIFY=varify,
                                                                   ALL_REPO=all_repo,
                                                                   FANS_TOTAL=fans_total,
                                                                   FOLLOW_TOTAL=follow_total,
                                                                   CLOSE_FANS=c_f,
                                                                   AVATAR_URL=avatar_url)
                            now_request_user = tf.readline()
                            if now_request_user[:-1] == '' or now_request_user == '':
                                print('[Info]Now user finished.Now mine next user.')
                                break
                        except:
                            print('[Warning]find an error that cannot be located.Meltdown mechanism might be touch off.sleep some time.(code 1)')
                            sleep(300+random())

                    tf.close()
                    self.sql_manager.flag_user_finished(get_a_new_user)
            except:
                print('[Warning]find an error that cannot be located.Meltdown mechanism might be touch off.sleep some time.(code 2)')
                sleep(600+random())


            # if not get_a_new_user:
            #     enter_user_id = raw_input('>>>enter an id')
            #     weibo_user_id = enter_user_id
            # else:
            #     weibo_user_id = get_a_new_user

if __name__ == '__main__':

    us = UserSpider()
    us.run()












