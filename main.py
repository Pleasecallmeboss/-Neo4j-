from GetDataFromJson import *
from NetEaseCloud_KnowledgeGraph import *
# import jieba
# jieba.load_userdict("dict.txt")
# import jieba.posseg as pseg

from Question_Classifier import *
from Question_Parse import *
from Question_Answer import *


def clean_all():
    cypher = "MATCH (n) detach delete n"
    app.cyphertx(cypher)

def insert():
    Dirs = getDirList(".\\Data_Lyric")
    for dir in Dirs:
        dirs = getDirList(dir)
        for d in dirs:
            files = getFileList(d)
            for f in files:
                json = GetDataFromJson(f)
                print()
                opt = app.getOption(
                    json['singer'], json['song_name'])
                app.create_Relationship(
                    json['singer'],
                    "Singer",
                    json['song_name'],
                    "Song",
                    "Singing",
                    opt)

                opt = app.getOption(
                    json['write_music'],
                    json['song_name'])
                app.create_Relationship(
                    json['write_music'],
                    "Composer",
                    json['song_name'],
                    "Song",
                    "Compose",
                    opt)

                opt = app.getOption(
                    json['write_words'],
                    json['song_name'])
                app.create_Relationship(
                    json['write_words'],
                    "Lyric_Writer",
                    json['song_name'],
                    "Song",
                    "Lyrics",
                    opt)

def ques_and_answer():
    question = input('input an question:')
    words = pseg.cut("AJ张杰演唱的歌曲有哪些")  # jieba默认模式
    dicts = []
    for word in words:
        word_str = str(word)
        word_split = word_str.split('/')
        if (word_split[1] == 'v' or word_split[1] == 'nr' or word_split[1] == 'n'):
            word_dict = {"Word": word_split[0], "PartOfSpeech": word_split[1]}
        else:
            continue
        dicts.append(word_dict)

    app.query(dicts)


def end():
    app.close()

def ques_and_answer_for_actree():
    # 1.AJ张杰唱的歌有哪些
    # 2.AJ张杰唱的、AlanWalker作曲的歌有哪些
    # 3.谁唱过AJ张杰唱过的歌 (AJ张杰唱过谁作词的歌)
    # 4.AJ张杰唱过谁作词的歌
    # 5.AJ张杰唱过《别说再见》吗
    # 6.和《大明星》相同作曲的歌曲
    handler = QuestionPaser()
    QChandler = QuestionClassifier()
    searcher = AnswerSearcher()

    while 1:
        question = input('input an question:')
        data = QChandler.classify(question)
        # print(data)
        sqls = handler.parser_main(data)
        # print(sqls)
        res = searcher.search_main(sqls)
        print(res)

if __name__ == '__main__':
    scheme = "bolt"  # Connecting to Aura, use the "neo4j+s" URI scheme
    host_name = "localhost"
    port = 7687
    url = "{scheme}://{host_name}:{port}".format(
        scheme=scheme, host_name=host_name, port=port)
    user = "neo4j"
    password = "neo4jjj"
    app = App(url, user, password)
    # clean_all()
    # insert()

    # while 1:
    #     # ques_and_answer()
    ques_and_answer_for_actree()
    end()
