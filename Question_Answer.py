#!/usr/bin/env python3
# coding: utf-8
# File: answer_search.py
# Author: lhy<lhy_in_blcu@126.com,https://huangyong.github.io>
# Date: 18-10-5
from neo4j import GraphDatabase
class AnswerSearcher:
    def __init__(self):
        uri = "bolt://localhost:7687"
        self.driver = GraphDatabase.driver(uri, auth=("neo4j", "neo4jjj"))
    def close(self):
        # Don't forget to close the driver connection when you are finished with it
        self.driver.close()
    def cyphertx(self,cypher):
        with self.driver.session() as session:
            with session.begin_transaction() as tx:
                tx.run(cypher)
                print("语句执行成功")
    def find_thing(self, query ):
        with self.driver.session() as session:
            result = session.read_transaction(self._find_and_return_thing, query)
            # if(result == []):
                # print("Not Found!")

            # else:
                # for record in result:
                #     print("Found {record}".format(record=record))
            return result



    @staticmethod
    def _find_and_return_thing(tx, query ):

        result = tx.run(query)
        return [record['name'] for record in result]


    '''执行cypher查询，并返回相应结果'''
    def search_main(self, sqls):
        answers = []


        for sql_ in sqls:
            question_type = sql_['question_type']
            queries = sql_['sql']
            res = self.find_thing(queries)
            # print(res)
            answers.append(res)
        answer = self.answer_prettify(question_type, answers)

        return answer



    '''根据对应的qustion_type，调用相应的回复模板'''
    def answer_prettify(self, question_type, answers):
        final_answer = []
        if not answers:
            return ''
        if question_type == 'double_condition':
            c = set(answers[0])
            for record in answers:
                c = c & set(record)
            return list(c)

        elif question_type == 'therearewhat':
            answers = list(set(answers[0]))
            return answers

        elif question_type == 'who':
            answers = list(set(answers[0]))
            return answers

        elif question_type == 'yes_or_no':
            if(answers != [[]]):
                return "YES"
            else:
                return "NO"


        elif question_type == 'same_part':
            answers = list(set(answers[0]))
            return answers



if __name__ == '__main__':
    # [{'question_type': 'therearewhat',
    #   'sql': "MATCH (m),(m)-[:Singing]->(n) where m.name = 'AJ张杰' return n.name as name"}]

    # [{'question_type': 'therearewhat',
    #   'sql': "MATCH (m),(m)-[:Singing]->(n) where m.name = 'AJ张杰' return n.name as name"},
    #  {'question_type': 'double_condition',
    #   'sql': "MATCH (m),(m)-[:Lyrics]->(n) where m.name = 'AlanWalker' return n.name as name"}]

    # [{'question_type': 'who',
    #   'sql': "MATCH (m)-[:Singing]->(n),(r)-[:Singing]->(n) where m.name = 'AJ张杰' return r.name as name"}]

    # [{'question_type': 'who',
    #   'sql': "MATCH (m)-[:Singing]->(n),(r)-[:Lyrics]->(n) where m.name = 'AJ张杰' return r.name as name"}]

    # [{'question_type': 'yes_or_no',
    #   'sql': "MATCH (m)-[:Singing]->(n) where m.name = 'AJ张杰' and n.name = '大明星' return n.name as name"}]

    # [{'question_type': 'same_part',
    #   'sql': " MATCH (m)-[:Compose]->(n), (m)-[:Compose]->(r) where n.name = '大明星' return r.name as name "}]

    searcher = AnswerSearcher()
    data = [{'question_type': 'same_part','sql': " MATCH (m)-[:Compose]->(n), (m)-[:Compose]->(r) where n.name = '大明星' return r.name as name "}]

    res = searcher.search_main(data)
    print(res)