#!/usr/bin/env python3
# coding: utf-8
# File: question_parser.py
# Author: lhy<lhy_in_blcu@126.com,https://huangyong.github.io>
# Date: 18-10-4
import os


class QuestionPaser:

    def __init__(self):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        #　特征词路径
        self.Singing_path = os.path.join(cur_dir, 'dict/Singing.txt')
        self.Compose_path = os.path.join(cur_dir, 'dict/Compose.txt')
        self.Lyrics_path = os.path.join(cur_dir, 'dict/Lyrics.txt')

        self.Singer_path = os.path.join(cur_dir, 'dict/Singer.txt')
        self.Composer_path = os.path.join(cur_dir, 'dict/Composer.txt')
        self.Lyric_Writer_path = os.path.join(cur_dir, 'dict/Lyric_Writer.txt')
        self.Song_path = os.path.join(cur_dir, 'dict/Song.txt')
        # 加载特征词
        self.Singing_wds= [i.strip() for i in open(self.Singing_path,encoding='utf-8') if i.strip()]
        self.Compose_wds= [i.strip() for i in open(self.Compose_path,encoding='utf-8') if i.strip()]
        self.Lyrics_wds= [i.strip() for i in open(self.Lyrics_path,encoding='utf-8') if i.strip()]
        self.Singer_wds = [i.strip() for i in open(self.Singer_path, encoding='utf-8') if i.strip()]
        self.Composer_wds = [i.strip() for i in open(self.Composer_path, encoding='utf-8') if i.strip()]
        self.Lyric_Writer_wds = [i.strip() for i in open(self.Lyric_Writer_path, encoding='utf-8') if i.strip()]
        self.Song_wds= [i.strip() for i in open(self.Song_path,encoding='utf-8') if i.strip()]

    '''构建实体节点'''
    def build_entitydict(self, args):
        entity_dict = {}
        for arg, types in args.items():
            if(arg in self.Singing_wds):
                arg = "Singing"
            elif(arg in self.Compose_wds):
                arg = "Compose"
            elif(arg in self.Lyrics_wds):
                arg = "Lyrics"

            elif (arg in self.Composer_wds):
                arg = "Composer"
            elif (arg in self.Lyric_Writer_wds):
                arg = "Lyric_Writer"
            elif (arg in self.Singer_wds):
                arg = "Singer"
            elif (arg in self.Song_wds):
                arg = "Song"
            for type in types:
                if type not in entity_dict:
                    entity_dict[type] = [arg]
                else:
                    entity_dict[type].append(arg)
        return entity_dict
    # {症状：头痛(咳嗽)}

    '''解析主函数'''
    def parser_main(self, res_classify):
        args = res_classify['args']
        entity_dict = self.build_entitydict(args)
        question_types = res_classify['question_types']
        sqls = []
        for question_type in question_types:
            sql_ = {}
            sql_['question_type'] = question_type
            sql = ""
            if question_type == 'disease_symptom':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))

            elif question_type == 'therearewhat':
                sql = self.sql_transfer(question_type, entity_dict)

            elif question_type == 'double_condition':
                sql = self.sql_transfer(question_type, entity_dict)

            elif question_type == 'who':
                sql = self.sql_transfer(question_type, entity_dict)

            elif question_type == 'yes_or_no':
                sql = self.sql_transfer(question_type, entity_dict)

            elif question_type == 'same_part':
                sql = self.sql_transfer(question_type, entity_dict)
            if sql:
                sql_['sql'] = sql

                sqls.append(sql_)
        return sqls

    '''针对不同的问题，分开进行处理'''
    def sql_transfer(self, question_type, entities):
        if not entities:
            return ""

        # 查询语句
        sql = ""
        # 根据条件查询并列出
        if question_type == 'therearewhat':
            sql = "MATCH (m),(m)-[:{0}]->(n) where m.name = '{1}' return n.name as name".format(entities.get('action')[0],entities.get('name')[0])
            print(sql)

        # 根据条件查询并列出
        elif question_type == 'double_condition':
            sql = "MATCH (m),(m)-[:{0}]->(n) where m.name = '{1}' return n.name as name".format(entities.get('action')[1],entities.get('name')[-1])
            print(sql)
        # 根据条件查询并列出
        elif question_type == 'who':
            sql = "MATCH (m)-[:{0}]->(n),(r)-[:{1}]->(n) where m.name = '{2}' return r.name as name".format(entities.get('action')[0],entities.get('action')[-1], entities.get('name')[0])
            print(sql)
        # 根据条件查询
        elif question_type == 'yes_or_no':
            sql = "MATCH (m)-[:{0}]->(n) where m.name = '{1}' and n.name = '{2}' return n.name as name".format(entities.get('action')[0],entities.get('name')[0], entities.get('name_song')[0])
            print(sql)
        # 根据条件查询
        elif question_type == 'same_part':
            sql = " MATCH (m)-[:{0}]->(n), (m)-[:{0}]->(r) where n.name = '{1}' return r.name as name ".format(entities.get('action')[0],entities.get('name_song')[0])
            print(sql)
        return sql



if __name__ == '__main__':
    # {'args': {'AJ张杰': ['singer_name'], '唱': ['action'], '歌': ['occupation']}, 'question_types': ['therearewhat']}
    # {'args': {'AJ张杰': ['name'], '唱': ['action'], 'AlanWalker': ['name'], '作词': ['action'], '歌': ['occupation']}, 'question_types': ['therearewhat', 'double_condition']}
    #{'args': {'唱': ['action'], 'AJ张杰': ['name'], '歌': ['occupation']}, 'question_types': ['who']}
    # {'args': {'AJ张杰': ['name'], '唱': ['action'], '作词': ['action'], '歌': ['occupation']}, 'question_types': ['who']}
    # {'args': {'AJ张杰': ['name'], '唱': ['action'], '别说再见': ['name_song']}, 'question_types': ['yes_or_no']}
    # {'args': {'大明星': ['name_song'], '作曲': ['action'], '歌曲': ['occupation']}, 'question_types': ['same_part']}
    handler = QuestionPaser()
    data = {'args': {'AJ张杰': ['name'], '唱': ['action'], '别说再见': ['name_song']}, 'question_types': ['yes_or_no']}



    sqls = handler.parser_main(data)
    print(sqls)

