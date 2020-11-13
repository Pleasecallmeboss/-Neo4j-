
from GetDataFromJson import getFileList,getDirList
import json
import os

def GetDataFromJson_(filename):
    fpath, fname = os.path.split(filename)
    name = fname.split(".")
    with open(filename,'r',encoding='utf-8-sig')as fp:
        strF = fp.read()
        if len(strF) > 0:
            json_data = json.loads(strF)
        else:
            json_data = {}
        json_data["song_name"] = name[0]

        print('这是文件中的json数据：', json_data)
        return json_data

def WriteFileFromJson(json):
    if(json.get('singer') or json.get('write_music') or json.get('write_words') not in name_set):
        with open(".\\dict\\name.txt", 'a', encoding='utf-8-sig')as fp:
            if (json.get('singer') not in name_set):
                name_set.add(json.get('singer'))
                strF = fp.write(json.get('singer') + '\n')
            if (json.get('write_music') not in name_set):
                name_set.add(json.get('write_music'))
                strF = fp.write(json.get('write_music') + '\n')
            if (json.get('write_words') not in name_set):
                name_set.add(json.get('write_words'))
                strF = fp.write(json.get('write_words') + '\n')


    if(json.get('song_name') not in name_song_set):
        name_song_set.add(json.get('song_name'))
        with open(".\\dict\\name_song.txt",'a',encoding='utf-8-sig')as fp:
            strF = fp.write(json.get('song_name')+'\n')




if __name__ == '__main__':

    name_set = set()
    name_song_set = set()
    Dirs = getDirList(".\\Data_Lyric")
    for dir in Dirs:
        dirs = getDirList(dir)
        for d in dirs:
            files = getFileList(d)
            for f in files:
                res = GetDataFromJson_(f)
                WriteFileFromJson(res)