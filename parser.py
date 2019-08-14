# coding:utf8
from bs4 import BeautifulSoup
import re
import sys
import json
reload(sys)
sys.setdefaultencoding('utf8')

# soup = BeautifulSoup(open('test_html.html'), 'lxml')
# print soup.select('div[class="c"]')[0]

class WeiboContentParser(object):
    def __init__(self, weibo_content):
        self.soup = BeautifulSoup(weibo_content, 'lxml')
        self.rule = re.compile('<a class="cc" href="(.*?)">评论\[(.*?)\]</a>', re.S)

    def get_user_weibo_content(self):
        weibo_list = [w.text for w in self.soup.select('div[class="c"]')]
        return weibo_list

    def get_total(self):
        # print(self.soup.prettify())
        weibo_info = self.soup.select('div[class="tip2"]')
        if weibo_info:
            weibo_info = weibo_info[0]
        else:
            print('[warning]cannot get user weibo amount')
            print(self.soup.prettify())
            return None

        r = BeautifulSoup(str(weibo_info), 'lxml')
        weibo_total_s = r.select('span[class="tc"]')[0].text
        weibo_total = int(weibo_total_s[3:-1])
        fans_total = None
        follow_total = None
        for item in r.select('a'):
            # print(item)
            if '关注' in str(item):
                follow_total = int(item.text[3:-1])
            if '粉丝' in str(item):
                fans_total = int(item.text[3:-1])
        print('[Info]Get User Info:', weibo_total, follow_total, fans_total)
        return weibo_total, follow_total, fans_total

    def get_cc_url(self):
        text_li = self.soup.select('div[class="c"]')
        url_list = []
        for item in text_li[:-2]:
            try:
                # print(item)
                c = BeautifulSoup(str(item), 'lxml').select('.cc')
                # print(c.prettify())
                # print(c[0])
                # print('h')
                # cc = self.rule.findall(str(item))
                cc = re.findall(r'href="(.*?)"', str(c[0]))
                # print(cc)
                if 'uid' in cc[0]:
                    url_list.append(cc[0])
            except:
                pass
        # print(url_list)
        return url_list

    def get_cc_url_li_to_string(self, split_sign='&;&;&;'):
        for i in self.get_user_weibo_content()[:-2]:
            print(i)
        li = self.get_cc_url()
        # print(li)
        s = ''
        for item in li:
            s += item + split_sign
        return s

    def get_weibo_content_to_string_and_all_repo(self, split_sign='&;//***//***//***&;'):
        s = ''
        all_repo = True
        for item in self.get_user_weibo_content()[:-2]:
            s += str(item) + split_sign
            # print(item)
            if not '转发了' in str(item):
                all_repo = False
        return s, all_repo


class UserInfoParser(object):
    def __init__(self, user_info_content):
        self.soup = BeautifulSoup(user_info_content, 'lxml')

    def get_user_info(self):
        avatar_url = None
        nickname = None
        gender = None
        addr = None
        birthday = None
        is_vip = None
        description = None
        education = None
        varify = None


        s = self.soup.select('div[class="c"]')
        for i in s:
            raw = unicode(i)
            # print('HERE')
            # print(raw)
            if '昵称' in raw:
                # print('here')
                try:
                    nickname = re.findall(u'>昵称:(.*?)<br/>', raw)[0]
                    # print(nickname)
                except:
                    print('[info]failed to scratch nickname')
                # print(nickname)
            if '性别' in raw:
                try:
                    gender = re.findall(u'性别:(.*?)<br/>', raw)[0]
                    # print(gender)
                except:
                    print('[info]failed to scratch gender')
                # print(gender)
            if '地区' in raw:
                try:
                    addr = re.findall(u'地区:(.*?)<br/>', raw)[0]
                    # print(addr)
                except:
                    print('[info]failed to scratch addr')
                # print(addr)
            if '生日' in raw:
                try:
                    birthday = re.findall(u'生日:(.*?)<br/>', raw)[0]
                    # print(birthday)
                except:
                    print('[info]failed to scratch birthday')
                # print(birthday)
            if '认证信息' in raw:
                try:
                    varify =re.findall(u'>认证:(.*?)<br/>', raw)[0]
                    # print(varify)
                except:
                    pass
                # print(varify)
            if '简介' in raw:
                try:
                    description = re.findall(u'>简介:(.*?)<br/>', raw)[0]
                    # print(description)
                except:
                    print('[info]failed to scratch description')
                # print(description)
            if '大学' in raw or '中学' in raw or '教育' in raw:
                try:
                    education = BeautifulSoup(raw, 'lxml').text
                    # print(education)
                except:
                    print('[info]failed to scratch education')
                # print(education)
            if '会员等级' in raw:
                try:
                    is_vip = re.findall(u'>会员等级：(.*?)级 <', raw)[0]
                except:
                    pass
                # print(is_vip)
            if '头像' in raw:
                try:
                    avatar_url = re.findall(u'src="(.*?)"', raw)[0]
                    # print(avatar_url)
                except:
                    print('[info]failed to scratch avatar url')
                # print(avatar_url)
        return avatar_url, nickname, gender, addr, birthday, is_vip, description, education, varify


class UserFansParser(object):
    def __init__(self, fans_contant):
        self.s = BeautifulSoup(fans_contant, 'lxml')

    def get_page_amount(self):
        try:
            pa = self.s.select('form')
            pa_text = str(pa[1].text)
            total_page = re.findall(u'.*?/(.*?)页', unicode(pa_text))[0]
            total_page = int(total_page)
            # print(pa)
            # print(total_page)
            return total_page
        except:
            print('[UserWarning]Get fans page faild.Now return 1.')
            return 1
        # print(re.findall(u'&nbsp;(.*?)/(.*?)页', str(self.s)))


    def get_fans_list(self):
        fans_li = []
        for item in self.s.select('td[valign="top"]')[1:]:
            # print(str(item))
            r = re.findall(r'<a href="https://weibo\.cn/u/(.*?)">.*?</a><br/>粉丝', str(item))
            if r:
                fans_li.append(r[0])
        # print(fans_li)
        return fans_li

    def get_fans_list_to_string(self, split_sign='&;'):
        fans_li = []
        for item in self.s.select('td[valign="top"]')[1:]:
            # print(str(item))
            r = re.findall(r'<a href="https://weibo\.cn/u/(.*?)">.*?</a><br/>粉丝', str(item))
            if r:
                fans_li.append(r[0])
        # print(fans_li)
        s = ''
        for item in fans_li:
            s += item + split_sign
        return s

class UserCCParser(object):

    def __init__(self, cc_content, weibo_user_id):
        self.s = BeautifulSoup(cc_content, 'lxml')
        self.weibo_user_id = weibo_user_id

    def get_close_fans(self):
        content_li = self.s.select('div[class="c"]')
        close_fans_li = []
        for item in content_li:
            weibo_id = re.findall('<a href="/u/([0-9]{10})">', str(item))
            if weibo_id:
                if weibo_id[0] != self.weibo_user_id:
                # print(weibo_id[0])
                    close_fans_li.append(weibo_id[0])
            # print(item)
        # print(self.s.prettify())
        # print(close_fans_li)
        return close_fans_li

    def get_close_fans_to_string(self, split_sign='&;'):
        close_fans_li = self.get_close_fans()
        s = ''
        for item in close_fans_li:
            s += str(item) + split_sign
        return s


class UserFansParserV2(object):
    def __init__(self, fans_content):
        self.fans_json = fans_content
        self.status = json.loads(fans_content)['ok']
        # print(self.status)
        self.r = re.compile('"uid":([0-9]{10}),', re.S)

    def get_flag(self):
        return self.status

    def get_fans_list(self):
        uid_li = self.r.findall(self.fans_json)
        return uid_li

    def get_fans_list_to_string(self, split_sign='&;'):
        s = ''
        for item in self.get_fans_list():
            s += item + split_sign
        return s

    def get_status(self):
        return self.status




if __name__ == '__main__':

    # ufp = UserFansParser(open('user_info_2.html'))
    # ufp.get_page_amount()
    # ufp.get_fans_list_to_string()
    # ucp = UserCCParser(cc_content=open('cc_html.html'), weibo_user_id='1')
    # print ucp.get_close_fans()
    # pass
    wcp = WeiboContentParser(open('test_html_5.html'))
    print wcp.get_total()
    # print(wcp.get_user_weibo_content())
    # print wcp.get_weibo_content_to_string()
    # print(wcp.run())
    # wcp.run()
    # s = wcp.get_weibo_content_to_string()
    # print(s)

    # uip = UserInfoParser(open('user_info_html_3.html'))
    # uip.get_user_info()





