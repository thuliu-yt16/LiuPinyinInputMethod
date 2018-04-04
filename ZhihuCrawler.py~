#coding=utf-8
import os,re,requests,urllib2,urllib,cookielib,json,time,random
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
        self.following_question_url = 'https://www.zhihu.com/api/v4/members/%(user_id)s/following-questions?include=data%%5B*%%5D.created%%2Canswer_count%%2Cfollower_count%%2Cauthor&offset=0&limit=20'
        self.user_answer_url = 'https://www.zhihu.com/api/v4/members/%(user_id)s/answers?include=data%%5B*%%5D.is_normal%%2Cadmin_closed_comment%%2Creward_info%%2Cis_collapsed%%2Cannotation_action%%2Cannotation_detail%%2Ccollapse_reason%%2Ccollapsed_by%%2Csuggest_edit%%2Ccomment_count%%2Ccan_comment%%2Ccontent%%2Cvoteup_count%%2Creshipment_settings%%2Ccomment_permission%%2Cmark_infos%%2Ccreated_time%%2Cupdated_time%%2Creview_info%%2Cquestion%%2Cexcerpt%%2Crelationship.is_authorized%%2Cvoting%%2Cis_author%%2Cis_thanked%%2Cis_nothelp%%2Cupvoted_followees%%3Bdata%%5B*%%5D.author.badge%%5B%%3F(type%%3Dbest_answerer)%%5D.topics&offset=0&limit=20&sort_by=created'

        self.followee_url = 'http://www.zhihu.com/api/v4/members/%(user_id)s/followees?include=data%%5B%%2A%%5D.answer_count%%2Carticles_count%%2Cgender%%2Cfollower_count%%2Cis_followed%%2Cis_following%%2Cbadge%%5B%%3F%%28type%%3Dbest_answerer%%29%%5D.topics&limit=20&offset=0'
        self.follower_url = 'http://www.zhihu.com/api/v4/members/%(user_id)s/followers?include=data%%5B%%2A%%5D.answer_count%%2Carticles_count%%2Cgender%%2Cfollower_count%%2Cis_followed%%2Cis_following%%2Cbadge%%5B%%3F%%28type%%3Dbest_answerer%%29%%5D.topics&limit=20&offset=0'
        self.save_path = u'D:/Course/Lessons/2018Spring/人工智能导论/LiuPinyinInputMethod/Zhihu/Text/'
        #self.save_path = 'Question_Id/'
        self.buffer = ''
        self.buffer_limit = 50000
        self.begin_user_id = ['zhang-jia-wei','excited-vczh','liu-ying-tian-65','bi-xiao-tian-99','jianghanchen']

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
        if 'error' in info_dic:
            return
        try:
            totals = info_dic['paging']['totals']
        except:
            print info_dic
            return
        if info_dic['paging']['is_end']:
            return
        if totals > 20:
            while(tot < count and tot < totals):
                for j in xrange(0,5):
                    try:
                        yield info_dic['data'][j]['content']
                        tot += 1
                        if tot >= count or tot > totals:
                            break
                    except (IndexError,KeyError):
                        continue
                url = self.next_page(url)
                r = self.get(url)
                info_dic = json.loads(r.text)
        else:
            return

    def get_question_id_from_user(self,user_id, count):
        url = self.user_answer_url%({'user_id':user_id})
        tot = 0
        r = self.get(url)
        info_dic = json.loads(r.text)
        totals = info_dic['paging']['totals']
        while(tot < count and tot < totals):
            for j in xrange(0,20):
                try:
                    print info_dic['data'][j]['question']['id']
                    yield info_dic['data'][j]['question']['id']
                    tot += 1
                    if tot >= count or tot >= totals:
                        break
                except (KeyError , IndexError):
                    pass
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
            new_list = []
            new_list += [followee for followee in self.get_followees_id_from_user(user_id,1000)]
            new_list += [follower for follower in self.get_followers_id_from_user(user_id,50000)]
            new_list = list(set(new_list))
            self.force_write(' '.join(new_list))

    def get_following_question_from_user_id(self,user_id, count):
        url = self.following_question_url%({'user_id':user_id})
        tot = 0
        r = self.get(url)
        info_dic = json.loads(r.text)
        try:
            totals = info_dic['paging']['totals']
        except KeyError:
            return
        is_read = 0
        if totals >= 20:
            while(tot < count and is_read < totals):
                for j in xrange(0,19):
                    print tot,is_read,totals
                    try:
                        if info_dic['data'][j]['answer_count'] > 100:
                            print info_dic['data'][j]['id']
                            yield info_dic['data'][j]['id']
                            tot += 1
                        is_read += 1
                        if tot >= count or is_read >= totals:
                            return
                    except (KeyError , IndexError):
                        is_read += 1
                        pass
                url = self.next_page(url)
                r = self.get(url)
                info_dic = json.loads(r.text)
        else:
            return

    '''
    def filter_user(self,user_id):
        url = self.following_question_url%({'user_id':user_id})
        r = self.get(url)
        info_dic = json.loads(r.text)
        totals = info_dic['paging']['totals']
        return totals >= 25
    '''

if __name__ == '__main__':
    crawler = Crawler()
    #with open('user_id_list.txt','r') as f:
    with open(u'D:/Course/Lessons/2018Spring/人工智能导论/LiuPinyinInputMethod/Zhihu/new_question_id_list.txt','r') as f:
        question_id_list = f.read().split(' ')

    pattern = re.compile(u"[\u4e00-\u9fa5]+")

    #random.shuffle(question_id_list)
    tot = 0
    for question_id in question_id_list:
        print 'tot:',tot,question_id
        result = []
        cnt = 0
        for answer in crawler.get_answer_from_question(question_id,500):
            s = re.findall(pattern,answer)
            if s:
                print s[0][0],
            result += s
            cnt += 1
            if cnt % 50 == 0:
                crawler.add_to_buffer(' '.join(result).encode('gbk'))
                result = []
        crawler.add_to_buffer(' '.join(result).encode('gbk'))
        tot += 1

        question_id_list.remove(question_id)
        with open(u'D:/Course/Lessons/2018Spring/人工智能导论/LiuPinyinInputMethod/Zhihu/new_question_id_list.txt','w') as f:
            f.write(' '.join(question_id_list))





