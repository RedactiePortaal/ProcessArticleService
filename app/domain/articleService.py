from app.repository.articleRepository import ArticleRepository


class ArticleService:
    def __init__(self, articleRepository: ArticleRepository):
        self.articleRepository = articleRepository

    def getArticleByTitle(self, title):
        pass
