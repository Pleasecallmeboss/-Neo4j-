# !/usr/bin/python
# -*- coding: utf-8 -*-


from neo4j import GraphDatabase

uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "neo4jjj"))


def cyphertx(cypher):
    with driver.session() as session:
        with session.begin_transaction() as tx:
            tx.run(cypher)


cypher = """
            create (Neo:Crew {name:'Neo'}),
                   (Morpheus:Crew {name: 'Morpheus'}),
                   (Trinity:Crew {name: 'Trinity'}),
                   (Cypher:Crew:Matrix {name: 'Cypher'}),
                   (Smith:Matrix {name: 'Agent Smith'}),
                   (Architect:Matrix {name:'The Architect'}),
                   (Neo)-[:KNOWS]->(Morpheus),
                   (Neo)-[:LOVES]->(Trinity),
                   (Morpheus)-[:KNOWS]->(Trinity),
                   (Morpheus)-[:KNOWS]->(Cypher),
                   (Cypher)-[:KNOWS]->(Smith),
                   (Smith)-[:CODED_BY]->(Architect)
         """  # "cypher from http://console.neo4j.org/"
if __name__ == '__main__':
    cyphertx(cypher)