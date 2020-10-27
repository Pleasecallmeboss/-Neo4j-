import json
import os


def GetDataFromJson(filename):
    fpath, fname = os.path.split(filename)
    name = fname.split(".")
    with open(filename,'r',encoding='utf-8-sig')as fp:
        strF = fp.read()
        if len(strF) > 0:
            json_data = json.loads(strF)
        else:
            json_data = {}
        json_data["song_name"] = name[0]
        try:
            del json_data["lyric_text"]
        except KeyError:
            print("没有此键值")

        #print('这是文件中的json数据：', json_data)
        return json_data



def getFileList(p):
    p = str(p)
    if p == "":
        return []
    p = p.replace("/", "\\")
    if p[-1] != "\\":
        a = os.listdir(p)
        p = p + "\\"
        b = [p+x for x in a if os.path.isfile(p + x)]
        #print(b)
        return b

def getDirList(p):
    p = str(p)
    if p == "":
        return []

    p = p.replace("/", "\\")

    if p[-1] != "\\":
        p = p + "\\"

    a = os.listdir(p)

    b = [p+x for x in a if os.path.isdir(p + x)]
    #print(b)
    return b



if __name__ == '__main__':
    Dirs = getDirList("E:\\Python_Projects\\Neo4j_PyCharm\\Data_Lyric")
    for dir in Dirs:
        dirs = getDirList(dir)
        for d in dirs:
            files = getFileList(d)
            for f in files:
                GetDataFromJson(f)


