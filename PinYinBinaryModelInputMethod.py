#coding=utf-8

import os,re,codecs
import cPickle as pickle


class PinyinInputMethod:
    char_dic = {}
    char_pair_dic = {}
    pinyin2char = {}
    total_char = 0
    total_char_pair = 0

    def __init__(self):
        self.char_dic,self.char_pair_dic = pickle.load(open(r'database/char_binary_model/char_dic','r')), pickle.load(open(r'database/char_binary_model/char_pair_dic','r'))
        self.pinyin2char = pickle.load(open(r'database/char_binary_model/pinyin2char_table','r'))

        self.total_char = sum([v for k,v in self.char_dic.items()])
        self.total_char_pair = sum([v for k,v in self.char_pair_dic.items()])
        print self.total_char,self.total_char_pair

        if self.char_dic and self.char_pair_dic and self.pinyin2char:
            print 'Init Done'
        else:
            print 'Init Error'

    def find_msp(self,sentence,lam):# lam is the smooth parameter
        cd = self.char_dic
        cpd = self.char_pair_dic
        p2c = self.pinyin2char
        tc = self.total_char
        tcp = self.total_char_pair

        def P(w1,w2 = ''):
            if w2:
                return (1-lam)*(cpd[(w1,w2)]if (w1,w2) in cpd else 0)*1.0/tcp + lam*(cd[w2] if w2 in cd else 0)*1.0/tc

            else:
                return (cd[w1] if w1 in cd else 0)*1.0/tc

        pinyin_list = sentence.split(' ')
        curr_sts_ps = [] #list of (sentence,last char, possibility)
        curr_char = [] #list of char of current pinyin
        nxt_sts_ps = []

        for pinyin in pinyin_list:
            curr_char = p2c[pinyin]
            if not curr_sts_ps:
                curr_sts_ps = [(c,c,P(c)) for c in curr_char]
            else:
                curr_sts_ps = [max([(sts_ps[0]+c, c, sts_ps[2]*P(sts_ps[1], c)) for sts_ps in curr_sts_ps],key = lambda x: x[2]) for c in curr_char]

        return max(curr_sts_ps,key = lambda x: x[2])[0]


if __name__ == '__main__':
    pinyin_input = PinyinInputMethod()
    print pinyin_input.find_msp('wo yao wen wen de xing fu',0)

