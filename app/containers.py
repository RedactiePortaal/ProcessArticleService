import urllib3
from dependency_injector import containers, providers
from neo4j import GraphDatabase

from app.config import Settings
from app.repository.articleRepository import ArticleRepository
from app.domain.articleService import ArticleService
from app.repository.nerRepository import NerRepository


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=["app.view.controller.articleController"])
    config = providers.Configuration()
    config.from_pydantic(Settings())

    # Context
    neo4jDriver = providers.Singleton(
        GraphDatabase.driver,
        uri=config.neo4j.uri(),
        auth=(config.neo4j.username(), config.neo4j.password())
    )
    httpClient = providers.Singleton(
        urllib3.PoolManager
    )

    # Repositories
    articleRepository = providers.Factory(
        ArticleRepository,
        neo4jDriver=neo4jDriver
    )

    nerRepository = providers.Factory(
        NerRepository,
        httpClient=httpClient,
        url=config.ner.url()
    )

    # Services
    articleService = providers.Factory(
        ArticleService,
        articleRepository=articleRepository,
        nerRepository=nerRepository
    )
