from datetime import datetime
from neo4j import GraphDatabase


class ArticleRepository:
    def __init__(self, neo4jDriver: GraphDatabase.driver):
        self.neo4jDriver = neo4jDriver

    def save(self, article: dict):
        unpackedAttributes = 'SET ' + ', '.join(
            f'article.{key}=\'{value}\'' for (key, value) in article.items())
        cypher = (f'CREATE (article:Article) \n'
                  'SET article.createdAt = $createdAt\n'
                  f'{unpackedAttributes}\n'
                  'RETURN article, LABELS(article) as labels, ID(article) as id')

        with self.neo4jDriver.session() as session:
            result = session.run(query=cypher,
                                 parameters={'createdAt': str(datetime.utcnow())})
        return result.data()[0]

    def getByProperty(self, propertyName: str, propertyValue: str):
        cypher = (f'Match (article)\n'
                  f'WHERE article.{propertyName} = \'{propertyValue}\'\n'
                  'RETURN ID(article) as id, LABELS(article) as labels, article')
        with self.neo4jDriver.session() as session:
            result = session.run(query=cypher)
        return result.data()

    def update(self, articleId: int, attributes: dict):
        cypher = '''MATCH (article) WHERE ID(article) = $id
                    SET article += $attributes
                    RETURN article, ID(article) as id, LABELS(article) as labels'''
        with self.neo4jDriver.session() as session:
            result = session.run(query=cypher,
                                 parameters={'id': articleId, 'attributes': attributes})

        return result.data()[0]

    def delete(self, ArticleId: int):
        cypher = '''MATCH (article)
                        WHERE ID(article) = $id
                        DETACH DELETE article'''

        with self.neo4jDriver.session() as session:
            result = session.run(query=cypher,
                                 parameters={'id': ArticleId})

            data = result.data()

        if not data:
            return True

        else:
            return data

    def addRelation(self, ArticleId: int, targetLabel: str, targetPropertyName: str,
                    targetPropertyValue: str, relationshipType: str):
        cypher = (f'MATCH (article) WHERE ID(article) = $id \n'
                  f'MATCH (targetNode:{targetLabel}) WHERE targetNode.{targetPropertyName} = $targetPropertyValue \n'
                  f'MERGE (article)-[r:{relationshipType}]->(targetNode)\n'
                  'SET r.createdAt = $createdAt\n'
                  'RETURN article, targetNode, LABELS(article), LABELS(targetNode), ID(article), ID(targetNode), '
                  'ID(r), TYPE(r), PROPERTIES(r)'
                  )
        with self.neo4jDriver.session() as session:
            result = session.run(query=cypher, parameters={
                'createdAt': str(datetime.utcnow()),
                'id': ArticleId,
                'targetPropertyValue': targetPropertyValue
            })
        return result.data()[0]
