#coding=utf-8
import os,re,requests,urllib2,urllib,cookielib,json,time
from bs4 import BeautifulSoup



class Crawler:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
            'authorization':'oauth c3cef7c66a1843f8b3a9e6a1e3160e20',
            'origin': 'https://www.zhihu.com',
            'referer': 'https://www.zhihu.com/signup?next=%2F',
        }
        self.session = requests.session()
        self.session.headers = self.headers
        self.session.cookies = cookielib.LWPCookieJar()
        
        self.question_url = 'https://www.zhihu.com/api/v4/questions/%(question_id)s/answers?sort_by=default&include=data%%5B%%2A%%5D.is_normal%%2Cadmin_closed_comment%%2Creward_info%%2Cis_collapsed%%2Cannotation_action%%2Cannotation_detail%%2Ccollapse_reason%%2Cis_sticky%%2Ccollapsed_by%%2Csuggest_edit%%2Ccomment_count%%2Ccan_comment%%2Ccontent%%2Ceditable_content%%2Cvoteup_count%%2Creshipment_settings%%2Ccomment_permission%%2Ccreated_time%%2Cupdated_time%%2Creview_info%%2Crelevant_info%%2Cquestion%%2Cexcerpt%%2Crelationship.is_authorized%%2Cis_author%%2Cvoting%%2Cis_thanked%%2Cis_nothelp%%2Cupvoted_followees%%3Bdata%%5B%%2A%%5D.mark_infos%%5B%%2A%%5D.url%%3Bdata%%5B%%2A%%5D.author.follower_count%%2Cbadge%%5B%%3F%%28type%%3Dbest_answerer%%29%%5D.topics&limit=5&offset=0'
        self.user_answer_url = 'https://www.zhihu.com/api/v4/members/%(user_id)s/answers?include=data%%5B*%%5D.is_normal%%2Cadmin_closed_comment%%2Creward_info%%2Cis_collapsed%%2Cannotation_action%%2Cannotation_detail%%2Ccollapse_reason%%2Ccollapsed_by%%2Csuggest_edit%%2Ccomment_count%%2Ccan_comment%%2Ccontent%%2Cvoteup_count%%2Creshipment_settings%%2Ccomment_permission%%2Cmark_infos%%2Ccreated_time%%2Cupdated_time%%2Creview_info%%2Cquestion%%2Cexcerpt%%2Crelationship.is_authorized%%2Cvoting%%2Cis_author%%2Cis_thanked%%2Cis_nothelp%%2Cupvoted_followees%%3Bdata%%5B*%%5D.author.badge%%5B%%3F(type%%3Dbest_answerer)%%5D.topics&offset=0&limit=20&sort_by=created'

        self.followee_url = 'http://www.zhihu.com/api/v4/members/%(user_id)s/followees?include=data%%5B%%2A%%5D.answer_count%%2Carticles_count%%2Cgender%%2Cfollower_count%%2Cis_followed%%2Cis_following%%2Cbadge%%5B%%3F%%28type%%3Dbest_answerer%%29%%5D.topics&limit=20&offset=0'
        self.follower_url = 'http://www.zhihu.com/api/v4/members/%(user_id)s/followers?include=data%%5B%%2A%%5D.answer_count%%2Carticles_count%%2Cgender%%2Cfollower_count%%2Cis_followed%%2Cis_following%%2Cbadge%%5B%%3F%%28type%%3Dbest_answerer%%29%%5D.topics&limit=20&offset=0'
        self.save_path = u'D:/Course/Lessons/2018Spring/人工智能导论/LiuPinyinInputMethod/Zhihu/user/'
        self.buffer = ''
        self.buffer_limit = 10000
        self.begin_user_id = ['zhang-jia-wei']

    '''
    def login(self):
        session = self.session
        r = session.get(self.url,headers = self.headers)
        soup = BeautifulSoup(r.text,'html.parser')
        print soup
        #info_dic = json.loads(r.text)
    '''

    def get(self,url):
        r = self.session.get(url,headers = self.headers)
        time.sleep(2)
        return r
    def add_to_buffer(self,text):
        l = len(self.buffer)
        if len(text) + l >= self.buffer_limit-1:
            self.buffer += text[:(self.buffer_limit - l)] + ' '
            with open(self.save_path + time.strftime('%y%m%d%H%M%S'),'w') as f:
                f.write(self.buffer)
            self.buffer = ''
            self.add_to_buffer(text[(self.buffer_limit - l):])
        else:
            self.buffer += text

    def force_write(self,text):
        with open(self.save_path + time.strftime('%y%m%d%H%M%S'),'w') as f:
            f.write(text)
    def next_page(self,url):
        limit = re.search(r'limit=(\d+)',url).groups()[0]
        offset = re.search(r'offset=(\d+)',url).groups()[0]
        return re.sub(r'offset=\d+','offset=' + str(eval(limit + '+' + offset)),url)

    def get_answer_from_question(self,question_id, count):
        url = self.question_url%({'question_id':question_id})
        tot = 0
        r = self.get(url)
        info_dic = json.loads(r.text)
        totals = info_dic['paging']['totals']

        while(tot < count and tot < totals):
            for j in xrange(0,5):
                yield info_dic['data'][j]['content'].encode('gbk','ignore')
                tot += 1
                if tot >= count or tot > totals:
                    break
            url = self.next_page(url)
            r = self.get(url)
            info_dic = json.loads(r.text)

    def get_question_id_from_user(self,user_id, count):
        url = self.user_answer_url%({'user_id':user_id})
        tot = 0
        r = self.get(url)
        info_dic = json.loads(r.text)
        totals = info_dic['paging']['totals']
        while(tot < count and tot < totals):
            for j in xrange(0,20):
                yield info_dic['data'][j]['question']['id']
                tot += 1
                if tot >= count or tot >= totals:
                    break
            url = self.next_page(url)
            r = self.get(url)
            info_dic = json.loads(r.text)

    def get_followees_id_from_user(self,user_id, count):
        session = self.session
        url = self.followee_url%({'user_id':user_id})
        tot = 0
        r = self.get(url)
        info_dic = json.loads(r.text)
        totals = info_dic['paging']['totals']

        while(tot < count and tot < totals):
            for j in xrange(0,20):
                print info_dic['data'][j]['url_token']
                yield info_dic['data'][j]['url_token']
                tot += 1
                if tot >= count or tot >= totals:
                    break
            url = self.next_page(url)
            r = self.get(url)
            info_dic = json.loads(r.text)

    def get_followers_id_from_user(self,user_id, count):
        session = self.session
        url = self.follower_url%({'user_id':user_id})
        tot = 0
        r = self.get(url)
        info_dic = json.loads(r.text)
        totals = info_dic['paging']['totals']

        while(tot < count and tot < totals):
            for j in xrange(0,20):
                print info_dic['data'][j]['url_token']
                yield info_dic['data'][j]['url_token']
                tot += 1
                if tot >= count or tot >= totals:
                    break
            url = self.next_page(url)
            r = self.get(url)
            info_dic = json.loads(r.text)


    def get_user(self):
        user_list = self.begin_user_id
        for user_id in user_list:
            self.force_write(' '.join([followee for followee in self.get_followees_id_from_user(user_id,1000)]))
            new_list = []
            cnt = 1
            for follower in self.get_followers_id_from_user(user_id,1000000):
                new_list.append(follower)
                cnt += 1
                if cnt % 10000 == 0 :
                    self.force_write(' '.join(new_list))
                    new_list = []
            self.force_write(' '.join(new_list))




        '''
        head = 0
        tail = 1
        while(tail < 100000):
            print [head,tail]
            new_list = []
            for i in xrange(head,tail):
                try:
                    for followee in self.get_followees_id_from_user(user_list[i],10):
                        if followee not in user_list:
                            new_list.append(followee)
                            print followee
                    for follower in self.get_followers_id_from_user(user_list[i],100):
                        if follower not in user_list:
                            new_list.append(follower)
                            print follower
                except KeyError:
                    pass
            new_list = list(set(new_list))
            head = tail
            tail += min(100,len(new_list))
            self.force_write(' '.join(new_list))
            user_list += new_list
        '''


crawler = Crawler()
with open(crawler.save_path + '1','w') as f:
    f.write('1')
crawler.get_user()



