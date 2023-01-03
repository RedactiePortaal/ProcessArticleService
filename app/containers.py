from dependency_injector import containers, providers
from neo4j import GraphDatabase

from app.repository.articleRepository import ArticleRepository
from app.domain.articleService import ArticleService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=["app.view.controller.articleController"])
    config = providers.Configuration(yaml_files=["config.yml"])

    neo4jDriver = providers.Singleton(
        GraphDatabase.driver,
        uri=config.uri,
        auth=(config.username, config.password)
    )

    articleRepository = providers.Factory(
        ArticleRepository,
        neo4jDriver=neo4jDriver
    )

    articleService = providers.Factory(
        ArticleService,
        articleRepository=articleRepository
    )
