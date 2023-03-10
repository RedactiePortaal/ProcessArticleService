from datetime import datetime
from typing import Optional, List

from neo4j import GraphDatabase

from app.repository.dto.node import Node
from app.repository.dto.relationship import Relationship


class ArticleRepository:
    def __init__(self, neo4jDriver: GraphDatabase.driver):
        self.neo4jDriver = neo4jDriver

    def save(self, article: dict) -> Node:
        unpackedAttributes = 'SET ' + ', '.join(
            f'article.{key}=\'{value}\'' for (key, value) in article.items())
        cypher = (f'CREATE (article:Article) \n'
                  'SET article.createdAt = $createdAt\n'
                  f'{unpackedAttributes}\n'
                  'RETURN article, LABELS(article) as labels, ID(article) as id')

        with self.neo4jDriver.session() as session:
            result = session.run(query=cypher,
                                 parameters={'createdAt': str(datetime.now())})
            data = result.data()[0]
        return Node(id=data['id'], labels=data['labels'], properties=data['article'])

    def getByProperty(self, propertyName: str, propertyValue: str) -> List[Node]:
        cypher = (f'Match (article)\n'
                  f'WHERE article.{propertyName} = \'{propertyValue}\'\n'
                  'RETURN ID(article) as id, LABELS(article) as labels, article')
        with self.neo4jDriver.session() as session:
            result = session.run(query=cypher)
            data = result.data()
            nodeList = []
            for node in data:
                node = Node(id=node['id'], labels=node['labels'], properties=node['article'])
                nodeList.append(node)
        return nodeList

    def getById(self, id: int) -> Optional[Node]:
        cypher = '''Match (article)
                    WHERE ID(article) = $id
                    RETURN ID(article) as id, LABELS(article) as labels, article'''
        with self.neo4jDriver.session() as session:
            result = session.run(query=cypher,
                                 parameters={'id': id})
            data = result.data()
            if not data:
                return
            data = result.data()[0]
        return Node(id=data['id'], labels=data['labels'], properties=data['article'])

    def update(self, articleId: int, attributes: dict):
        cypher = '''MATCH (article) WHERE ID(article) = $id
                    SET article += $attributes
                    RETURN article, ID(article) as id, LABELS(article) as labels'''
        with self.neo4jDriver.session() as session:
            result = session.run(query=cypher,
                                 parameters={'id': articleId, 'attributes': attributes})
            data = result.data()[0]
        return data

    def delete(self, articleId: int):
        cypher = '''MATCH (article)
                        WHERE ID(article) = $id
                        DETACH DELETE article'''

        with self.neo4jDriver.session() as session:
            result = session.run(query=cypher,
                                 parameters={'id': articleId})

            data = result.data()

        if not data:
            return True

        else:
            return data

    def addRelationIncoming(self, ArticleId: int, targetLabel: str, targetPropertyName: str,
                            targetPropertyValue: str, relationshipType: str) -> Relationship:
        cypher = (f'MATCH (article) WHERE ID(article) = $id \n'
                  f'MERGE (targetNode:{targetLabel}{{{targetPropertyName}:$targetPropertyValue}})\n'
                  f'MERGE (article)<-[r:{relationshipType}]-(targetNode)\n'
                  'SET r.createdAt = $createdAt\n'
                  'RETURN article, targetNode, LABELS(article), LABELS(targetNode), ID(article), ID(targetNode),  ID(r), TYPE(r), PROPERTIES(r)'
                  )
        with self.neo4jDriver.session() as session:
            result = session.run(query=cypher, parameters={
                'createdAt': str(datetime.now()),
                'id': ArticleId,
                'targetPropertyValue': targetPropertyValue
            })
            relationshipData = result.data()[0]
            articleNode = Node(id=relationshipData['ID(article)'],
                               labels=relationshipData['LABELS(article)'],
                               properties=relationshipData['article'])
            targetNode = Node(id=relationshipData['ID(targetNode)'],
                              labels=relationshipData['LABELS(targetNode)'],
                              properties=relationshipData['targetNode'])
            relationshipNode = Relationship(id=relationshipData['ID(r)'],
                                            type=relationshipData['TYPE(r)'],
                                            properties=relationshipData['PROPERTIES(r)'],
                                            source=articleNode,
                                            target=targetNode)
        return relationshipNode

    def addRelationOutgoing(self, ArticleId: int, targetLabel: str, targetPropertyName: str,
                            targetPropertyValue: str, relationshipType: str) -> Relationship:
        cypher = (f'MATCH (article) WHERE ID(article) = $id \n'
                  f'MERGE (targetNode:{targetLabel}{{{targetPropertyName}:$targetPropertyValue}})\n'
                  f'MERGE (article)-[r:{relationshipType}]->(targetNode)\n'
                  'SET r.createdAt = $createdAt\n'
                  'RETURN article, targetNode, LABELS(article), LABELS(targetNode), ID(article), ID(targetNode),  ID(r), TYPE(r), PROPERTIES(r)'
                  )
        with self.neo4jDriver.session() as session:
            result = session.run(query=cypher, parameters={
                'createdAt': str(datetime.now()),
                'id': ArticleId,
                'targetPropertyValue': targetPropertyValue
            })
            relationshipData = result.data()[0]
            articleNode = Node(id=relationshipData['ID(article)'],
                               labels=relationshipData['LABELS(article)'],
                               properties=relationshipData['article'])
            targetNode = Node(id=relationshipData['ID(targetNode)'],
                              labels=relationshipData['LABELS(targetNode)'],
                              properties=relationshipData['targetNode'])
            relationshipNode = Relationship(id=relationshipData['ID(r)'],
                                            type=relationshipData['TYPE(r)'],
                                            properties=relationshipData['PROPERTIES(r)'],
                                            source=articleNode,
                                            target=targetNode)
        return relationshipNode

    def connectNodesById(self, sourceId, targetId, relationshipType):
        cypherExists = (f'MATCH (source) WHERE ID(source) = $source_id \n'
                        f'MATCH (target) WHERE ID(target) = $target_id \n'
                        f'MATCH (source)<-[r:{relationshipType}]-(target)\n'
                        'RETURN source, target, LABELS(source), LABELS(target), ID(source), ID(target),  ID(r), TYPE(r), PROPERTIES(r)'
                        )
        with self.neo4jDriver.session() as session:
            result = session.run(query=cypherExists, parameters={
                'source_id': sourceId,
                'target_id': targetId,
            })
            data = result.data()
            if data:
                return

            cypher = (f'MATCH (source) WHERE ID(source) = $source_id \n'
                      f'MATCH (target) WHERE ID(target) = $target_id \n'
                      f'MERGE (source)-[r:{relationshipType}]->(target)\n'
                      'SET r.createdAt = $createdAt\n'
                      'RETURN source, target, LABELS(source), LABELS(target), ID(source), ID(target),  ID(r), TYPE(r), PROPERTIES(r)'
                      )
            result = session.run(query=cypher, parameters={
                'createdAt': str(datetime.now()),
                'source_id': sourceId,
                'target_id': targetId,
            })
            data = result.data()
            if not data:
                return
            relationshipData = data[0]
            articleNode = Node(id=relationshipData['ID(source)'],
                               labels=relationshipData['LABELS(source)'],
                               properties=relationshipData['source'])
            targetNode = Node(id=relationshipData['ID(target)'],
                              labels=relationshipData['LABELS(target)'],
                              properties=relationshipData['target'])
            relationshipNode = Relationship(id=relationshipData['ID(r)'],
                                            type=relationshipData['TYPE(r)'],
                                            properties=relationshipData['PROPERTIES(r)'],
                                            source=articleNode,
                                            target=targetNode)

        return relationshipNode
