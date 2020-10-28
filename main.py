from GetDataFromJson import *
from NetEaseCloud_KnowledgeGraph import *


def app():
    scheme = "bolt"  # Connecting to Aura, use the "neo4j+s" URI scheme
    host_name = "localhost"
    port = 7687
    url = "{scheme}://{host_name}:{port}".format(
        scheme=scheme, host_name=host_name, port=port)
    user = "neo4j"
    password = "neo4jjj"
    app = App(url, user, password)
    cypher = "MATCH (n) detach delete n"
    app.cyphertx(cypher)
    Dirs = getDirList(".\\Data_Lyric")
    for dir in Dirs:
        dirs = getDirList(dir)
        for d in dirs:
            files = getFileList(d)
            for f in files:
                json = GetDataFromJson(f)
                print()
                opt = app.getOption(
                    json['singer'], "Singer", json['song_name'], "Song")
                app.create_Relationship(
                    json['singer'],
                    "Singer",
                    json['song_name'],
                    "Song",
                    "Singing",
                    opt)

                opt = app.getOption(
                    json['write_music'],
                    "Composer",
                    json['song_name'],
                    "Song")
                app.create_Relationship(
                    json['write_music'],
                    "Composer",
                    json['song_name'],
                    "Song",
                    "Compose",
                    opt)

                opt = app.getOption(
                    json['write_words'],
                    "Lyric_Writer",
                    json['song_name'],
                    "Song")
                app.create_Relationship(
                    json['write_words'],
                    "Lyric_Writer",
                    json['song_name'],
                    "Song",
                    "Lyrics",
                    opt)


# app.create_Relationship("Alice", "Singer", "飞云之上", "Song", "Singing")
# app.find_singer("Alice")

def end():
    app.close()


if __name__ == '__main__':
    app()
    end()
