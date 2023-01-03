from neo4j import GraphDatabase
from app.config import appConfig

appConfig.get('neo4j').get('uri')

neo4jDriver = GraphDatabase.driver(appConfig.get('neo4j').get('uri'),
                                   auth=(appConfig.get('neo4j').get('username'),
                                         appConfig.get('neo4j').get('password')))
