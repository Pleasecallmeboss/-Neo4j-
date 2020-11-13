import spacy
import jieba
jieba.load_userdict("dict.txt")
import jieba.posseg as pseg

def spacy_test():
    nlp = spacy.load('zh_core_web_sm')
    doc = nlp("周杰伦唱的歌曲有哪些，周杰伦作词的歌曲有哪些")
    print(nlp.pipe_names)
    # nlp.disable_pipes('tagger','parser')
    # print(nlp.pipe_names)
    # 将文章切分成句子 sentencizer
    print("分句 sentencizer")
    for token in doc.sents:
        print(token.text)
    # 分词
    print("分词 Tokenization")
    for token in doc:
        print(token.text)
    # 词性标注
    print("词性标注 Part-of-speech tagging")
    for token in doc:
        print(token.text,"-->",token.pos_)
    print(spacy.explain("PRON"))
    # 词性还原
    print("词性还原 Lemmatization")
    for token in doc:
        print(token.text,"-->",token.lemma_)
    # 识别停用词
    print("识别停用词 Stop words")
    for token in doc:
        print(token.text,"-->",token.is_stop)
    # 依存分析
    print("依存分析 Dependency Parsing")
    for token in doc:
        print(token.text,"-->",token.dep_)
    # 提取名词短语
    print("提取名词短语 Noun Chunks")
    for token in doc.noun_chunks:
        print(token)
    # 命名实体识别
    print("命名实体识别")
    for token in doc.ents:
        print(token.text,"-->",token.label_)

def jieba_test(question):
    # jieba.add_word('唱 5 v')
    # jieba.add_word('歌 6 n')

    words = pseg.cut(question)  # jieba默认模式
    # for word in words:
    #     print(word)
    # jieba.enable_paddle()  # 启动paddle模式。 0.40版之后开始支持，早期版本不支持
    # words = pseg.cut("我爱北京天安门", use_paddle=True)  # paddle模式
    # for word, flag in words:
    #     print(word,"-->",flag)
    dicts = []
    for word in words:
        word_str = str(word)
        word_split = word_str.split('/')
        if (word_split[1] == 'v' or word_split[1] == 'nr' or word_split[1] == 'n'):
            word_dict = {"Word": word_split[0], "PartOfSpeech": word_split[1]}
        else:
            continue
        dicts.append(word_dict)
    return dicts
if __name__ == '__main__':
    # spacy_test()
    # jieba_test("AJ张杰演唱的，张杰作词的歌曲有哪些")
    question = input("key")
