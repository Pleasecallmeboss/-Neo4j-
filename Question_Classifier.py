#!/usr/bin/env python3
# coding: utf-8
# File: question_classifier.py
# Author: lhy<lhy_in_blcu@126.com,https://huangyong.github.io>
# Date: 18-10-4

import os
import ahocorasick

class QuestionClassifier:
    def __init__(self):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        #　特征词路径
        self.name_path = os.path.join(cur_dir, 'dict/name.txt')
        self.name_song_path = os.path.join(cur_dir, 'dict/name_song.txt')

        self.Singing_path = os.path.join(cur_dir, 'dict/Singing.txt')
        self.Compose_path = os.path.join(cur_dir, 'dict/Compose.txt')
        self.Lyrics_path = os.path.join(cur_dir, 'dict/Lyrics.txt')

        self.Singer_path = os.path.join(cur_dir, 'dict/Singer.txt')
        self.Composer_path = os.path.join(cur_dir, 'dict/Composer.txt')
        self.Lyric_Writer_path = os.path.join(cur_dir, 'dict/Lyric_Writer.txt')
        self.Song_path = os.path.join(cur_dir, 'dict/Song.txt')

        # 加载特征词
        self.name_wds= [i.strip() for i in open(self.name_path, encoding='utf-8') if i.strip()]
        self.name_song_wds= [i.strip() for i in open(self.name_song_path, encoding='utf-8') if i.strip()]

        self.Singing_wds= [i.strip() for i in open(self.Singing_path,encoding='utf-8') if i.strip()]
        self.Compose_wds= [i.strip() for i in open(self.Compose_path,encoding='utf-8') if i.strip()]
        self.Lyrics_wds= [i.strip() for i in open(self.Lyrics_path,encoding='utf-8') if i.strip()]

        self.Singer_wds= [i.strip() for i in open(self.Singer_path,encoding='utf-8') if i.strip()]
        self.Composer_wds= [i.strip() for i in open(self.Composer_path,encoding='utf-8') if i.strip()]
        self.Lyric_Writer_wds= [i.strip() for i in open(self.Lyric_Writer_path,encoding='utf-8') if i.strip()]
        self.Song_wds= [i.strip() for i in open(self.Song_path,encoding='utf-8') if i.strip()]


        self.region_words = set(self.name_wds + self.name_song_wds + self.Singing_wds + self.Compose_wds + self.Lyrics_wds + self.Singer_wds + self.Composer_wds + self.Lyric_Writer_wds + self.Song_wds)
        # 构造领域actree
        self.region_tree = self.build_actree(list(self.region_words))
        # 构建词典
        self.wdtype_dict = self.build_wdtype_dict()
        # 问句疑问词
        self.therearewhat_qwds = ['有哪些']
        self.double_condition_qwds = ['并且', '、']
        self.who_qwds = ['谁']
        self.yes_or_no_qwds = ['吗']
        self.same_part_qwds = ['相同']
        print('model init finished ......')

        return

    '''分类主函数'''
    def classify(self, question):
        data = {}
        question_dict = self.check_medical(question)
        if(question_dict == {}):
            print("找不到关键词")
            return
        # if not question_dict:
        #     if 'question_alltime_dict' in globals():    # 判断是否是首次提问，
        #         question_dict = question_alltime_dict
        #     else:
        #         return {}
        print("question_dict : ", question_dict)
        data['args'] = question_dict
        #收集问句当中所涉及到的实体类型
        types = []
        for type_ in question_dict.values():
            types += type_

        question_types = []

        # 列举歌曲
        if self.check_words(self.therearewhat_qwds, question) :
            question_type = 'therearewhat'
            question_types.append(question_type)
        # 双重条件列举歌曲
        if self.check_words(self.double_condition_qwds, question):
            question_type = 'double_condition'
            question_types.append(question_type)
        # 谁唱过AJ张杰唱过的歌 AJ张杰唱过谁作词的歌
        if self.check_words(self.who_qwds, question):
            question_type = 'who'
            question_types.append(question_type)
        # 询问是否完成过
        if self.check_words(self.yes_or_no_qwds, question):
            question_type = 'yes_or_no'
            question_types.append(question_type)
        # 具有相同的部分
        if self.check_words(self.same_part_qwds, question):
            question_type = 'same_part'
            question_types.append(question_type)


        # 若没有查到相关信息，返回NO
        if question_types == []:
            question_types = ['NO']

        # 将多个分类结果进行合并处理，组装成一个字典
        data['question_types'] = question_types

        return data

    '''构造词对应的类型'''
    def build_wdtype_dict(self):
        wd_dict = dict()
        for wd in self.region_words:
            wd_dict[wd] = []
            if wd in self.name_wds:
                wd_dict[wd].append('name')
            if wd in self.name_song_wds:
                wd_dict[wd].append('name_song')
            if wd in self.Singing_wds:
                wd_dict[wd].append('action')
            if wd in self.Compose_wds:
                wd_dict[wd].append('action')
            if wd in self.Lyrics_wds:
                wd_dict[wd].append('action')
            if wd in self.Singer_wds:
                wd_dict[wd].append('occupation')
            if wd in self.Composer_wds:
                wd_dict[wd].append('occupation')
            if wd in self.Lyric_Writer_wds:
                wd_dict[wd].append('occupation')
            if wd in self.Song_wds:
                wd_dict[wd].append('occupation')

        return wd_dict

    '''构造actree，加速过滤'''
    def build_actree(self, wordlist):
        actree = ahocorasick.Automaton()         # 初始化trie树
        for index, word in enumerate(wordlist):
            actree.add_word(word, (index, word))     # 向trie树中添加单词
        actree.make_automaton()    # 将trie树转化为Aho-Corasick自动机
        return actree

    '''问句过滤'''
    def check_medical(self, question):
        region_wds = []
        for i in self.region_tree.iter(question):   # ahocorasick库 匹配问题  iter返回一个元组，i的形式如(3, (23192, '乙肝'))
            # 第一个参数作用 ？
            wd = i[1][1]      # 匹配到的词
            region_wds.append(wd)
        stop_wds = []
        for wd1 in region_wds:
            for wd2 in region_wds:
                if wd1 in wd2 and wd1 != wd2:
                    stop_wds.append(wd1)       # stop_wds取重复的短的词，如region_wds=['乙肝', '肝硬化', '硬化']，则stop_wds=['硬化']
        final_wds = [i for i in region_wds if i not in stop_wds]     # final_wds取长词
        final_dict = {i:self.wdtype_dict.get(i) for i in final_wds}  # 获取词和词所对应的实体类型
        # global question_alltime_dict
        # if final_dict:
        #     question_alltime_dict = final_dict
        # print("final_dict : ",final_dict)
        # if 'question_alltime_dict' in globals():
        #     print("question_alltime_dict : ",question_alltime_dict)
        # else:
        #     print("question_alltime_dict does not exist.")
        return final_dict

    '''基于特征词进行分类'''
    def check_words(self, wds, sent):
        for wd in wds:
            if wd in sent:
                return True
        return False


if __name__ == '__main__':
    handler = QuestionClassifier()
    while 1:
        # AJ张杰唱的歌有哪些
        # AJ张杰唱的、AlanWalker作词的歌有哪些
        # 谁唱过AJ张杰唱过的歌 (AJ张杰唱过谁作词的歌)
        # AJ张杰唱过谁作词的歌
        # AJ张杰唱过《别说再见》吗
        # 和《大明星》相同作曲的歌曲

        question = input('input an question:')
        data = handler.classify(question)
        print(data)

