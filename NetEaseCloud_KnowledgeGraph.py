import logging
from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable

class App:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        # Don't forget to close the driver connection when you are finished with it
        self.driver.close()

    def cyphertx(self , cypher):
        with self.driver.session() as session:
            with session.begin_transaction() as tx:
                tx.run(cypher)
                print("语句执行成功")

    #创建演唱关系
    # def create_Singing(self, singername, songname):
    #     with self.driver.session() as session:
    #         # Write transactions allow the driver to handle retries and transient errors
    #         result = session.write_transaction(
    #             self._create_and_return_sing, singername, songname)
    #         for record in result:
    #             print("Created Singing between: {p1}, {p2}".format(
    #                 p1=record['p1'], p2=record['p2']))
    #
    # @staticmethod
    # def _create_and_return_sing(tx, singername, songname):
    #
    #     # To learn more about the Cypher syntax,
    #     # see https://neo4j.com/docs/cypher-manual/current/
    #
    #     # The Reference Card is also a good resource for keywords,
    #     # see https://neo4j.com/docs/cypher-refcard/current/
    #
    #     query = (
    #         "CREATE (p1:Singer { name: $singername }) "
    #         "CREATE (p2:Song { name: $songname }) "
    #         "CREATE (p1)-[:SINGING]->(p2) "
    #         "RETURN p1, p2"
    #     )
    #     result = tx.run(query, singername=singername, songname=songname)
    #     try:
    #         return [{"p1": record["p1"]["name"], "p2": record["p2"]["name"]}
    #                 for record in result]
    #     # Capture any errors along with the query and data for traceability
    #     except ServiceUnavailable as exception:
    #         logging.error("{query} raised an error: \n {exception}".format(
    #             query=query, exception=exception))
    #         raise
    #创建关系
    def create_Relationship(self, name_one, aswhat1, name_two, aswhat2,ship,option):
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            result = session.write_transaction(
                self._create_and_return_ship, name_one, aswhat1, name_two, aswhat2,ship,option)
            for record in result:
                print("Created {ship} between: {p1} and {p2}".format(
                    p1=record['p1'], p2=record['p2'],ship = record['ship']))

    @staticmethod
    def _create_and_return_ship(tx, name_one, aswhat1, name_two, aswhat2,ship,option):

        # To learn more about the Cypher syntax,
        # see https://neo4j.com/docs/cypher-manual/current/

        # The Reference Card is also a good resource for keywords,
        # see https://neo4j.com/docs/cypher-refcard/current/
        #1 for 都没有 2 for 前一个有 3 for 后一个有 4 for 都有
        query = " "
        query1 = (
            "CREATE (p1:" + aswhat1 + " { name: $name_one }) "
            "CREATE (p2:" + aswhat2 + " { name: $name_two }) "
            "CREATE (p1)-[:" + ship + "]->(p2) "
            "RETURN p1, p2 "
        )
        query2 = (
            "MATCH (p1)"
            "WHERE p1.name = $name_one "
            "SET p1:" + aswhat1 + " "
            "CREATE (p2:" + aswhat2 + " { name: $name_two }) "
            "CREATE (p1)-[:" + ship + "]->(p2) "
            "RETURN p1, p2 "
        )
        query3 = (
            "MATCH (p2)"
            "WHERE p2.name = $name_two "
            "SET p2:" + aswhat2 + " "
            "CREATE (p1:" + aswhat1 + " { name: $name_one }) "
            "CREATE (p1)-[:" + ship + "]->(p2) "
            "RETURN p1, p2 "
        )
        query4 = (
            "MATCH (p1) "
            "WHERE p1.name = $name_one "
            "MATCH (p2) "
            "WHERE p2.name = $name_two "
            "SET p1:" + aswhat1 + " "
            "SET p2:" + aswhat2 + " "
            "CREATE (p1)-[:" + ship + "]->(p2) "
            "RETURN p1, p2 "
        )
        if(option == 1):
            query = query1
        elif(option == 2):
            query = query2
        elif(option == 3):
            query = query3
        elif(option == 4):
            query = query4
        result = tx.run(query, name_one=name_one, aswhat1=aswhat1, name_two=name_two, aswhat2=aswhat2,ship=ship)
        try:
            return [{"p1": record["p1"]["name"], "p2": record["p2"]["name"] , "ship":ship}
                    for record in result]
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise



    # def find_singer(self, singer_name):
    #     with self.driver.session() as session:
    #         result = session.read_transaction(self._find_and_return_singer, singer_name)
    #         for record in result:
    #             print("Found singer: {record}".format(record=record))
    #
    # @staticmethod
    # def _find_and_return_singer(tx, singer_name):
    #     query = (
    #         "MATCH (p:Singer) "
    #         "WHERE p.name = $singer_name "
    #         "RETURN p.name AS name"
    #     )
    #     result = tx.run(query, singer_name=singer_name)
    #     return [record["name"] for record in result]

    def find_thing(self, name ):
        with self.driver.session() as session:
            result = session.read_transaction(self._find_and_return_thing, name)
            if(result == []):
                print("Not Found!")
                return False
            else:
                for record in result:
                    print("Found {aswhat} : {record}".format(record=record["name"], aswhat=record["label"]))
                return True



    @staticmethod
    def _find_and_return_thing(tx, name ):
        query = (
            "MATCH (p) "
            "WHERE p.name = $name "
            "RETURN p.name AS name,labels(p) AS label"
        )
        result = tx.run(query, name=name)
        return [{"name":record["name"], "label":record["label"]} for record in result]

    def getOption(self, name_one,name_two):
        a = self.find_thing(name_one)
        b = self.find_thing(name_two)
        if(a==False and b == False):
            return 1
        elif(a==True and b == False):
            return 2
        elif(a==False and b == True):
            return 3
        elif(a==True and b == True):
            return 4

    # match(d: Song), (a{name:"AJ张杰"})
    # where(a) - [: Singing]->(d)
    # return d.name
    def query(self, dicts):
        with self.driver.session() as session:
            result = session.read_transaction(self._query, dicts)
            if(result == [[]]):
                print("Not Found!")

            else:
                c = set(result[0])
                for record in result:
                    c = c&set(record)
                for ca in c:
                    print("Found {record}".format(record=ca))


            return result
    @staticmethod
    def _query(tx, dicts):
        nr = []
        v = []
        for dict in dicts:
            if(dict["PartOfSpeech"] == "nr"):
                nr.append("\""+dict["Word"]+"\"")
                # nr.append(dict["Word"])
            elif(dict["PartOfSpeech"] == "v"):
                if(dict["Word"] == "演唱"):
                    v.append("Singing")
                elif(dict["Word"] == "作词"):
                    v.append("Lyrics")
                elif(dict["Word"] == "作曲"):
                    v.append("Compose")
            elif (dict["PartOfSpeech"] == "n" and dict["Word"] == "歌曲"):
                n = "Song"
        num = len(nr)
        i = 0
        lists = []
        while(i != num):
            query = (
                "match(d: "+ n +"), (a{name:"+ nr[i] +"}) "
                "where(a) - [: "+ v[i] +"]->(d) "
                "return d.name as name"
            )
            result = tx.run(query)
            i= i+1
            lists.append([record["name"] for record in result])
        return lists

if __name__ == "__main__":
    # See https://neo4j.com/developer/aura-connect-driver/ for Aura specific connection URL.
    scheme = "bolt"  # Connecting to Aura, use the "neo4j+s" URI scheme
    host_name = "localhost"
    port = 7687
    url = "{scheme}://{host_name}:{port}".format(scheme=scheme, host_name=host_name, port=port)
    user = "neo4j"
    password = "neo4jjj"
    app = App(url, user, password)
    # cypher = "MATCH (n) detach delete n"
    # app.cyphertx(cypher)
    # opt = app.getOption("Alice","飞云之上")
    # app.create_Relationship("Alice","Composer","飞云之上","Song","Compose",opt)
    # opt = app.getOption("Bob", "飞云之上")
    # app.create_Relationship("Bob", "Composer", "飞云之上","Song", "Compose", opt)
    # opt = app.getOption("Alice", "你的故事")
    # app.create_Relationship("Alice","Singer","你的故事","Song","Singing",opt)
    #
    # app.find_thing("Alice")
    # app.find_thing("Bob")
    # app.find_thing("Composer", "Bob")
    # app.find_thing("Song","飞云之上")
    # app.find_thing("Song", "fei")
    #Singer Composer Lyric_Writer Song
    # app.find_singer("Alice")

    dict = [{'Word': 'AJ张杰', 'PartOfSpeech': 'nr'},
            {'Word': '演唱', 'PartOfSpeech': 'v'},
            {'Word': '张杰', 'PartOfSpeech': 'nr'},
            {'Word': '作曲', 'PartOfSpeech': 'v'},
            {'Word': '歌曲', 'PartOfSpeech': 'n'},
            {'Word': '有', 'PartOfSpeech': 'v'},
            ]
    app.query(dict)
    app.close()

