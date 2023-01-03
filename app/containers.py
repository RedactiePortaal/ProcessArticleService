from dependency_injector import containers, providers

from app.repository.articleRepository import ArticleRepository
from app.domain.articleService import ArticleService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=["app.view.controller.articleController"])
    articleRepository = providers.Factory(
        ArticleRepository
    )

    articleService = providers.Factory(
        ArticleService,
        articleRepository=articleRepository
    )
