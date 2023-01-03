from dependency_injector import containers, providers
from neo4j import GraphDatabase

from app.repository.articleRepository import ArticleRepository
from app.domain.articleService import ArticleService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=["app.view.controller.articleController"])
    config = providers.Configuration()
    config.from_json("./config.json")
    config2 = config.neo4j.uri()
    neo4jDriver = providers.Singleton(
        GraphDatabase.driver,
        uri=config.neo4j.uri(),
        auth=(config.neo4j.username(), config.neo4j.password())
    )

    articleRepository = providers.Factory(
        ArticleRepository,
        neo4jDriver=neo4jDriver
    )

    articleService = providers.Factory(
        ArticleService,
        articleRepository=articleRepository
    )
