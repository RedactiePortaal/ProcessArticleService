from app.domain.dto.processArticleDTO import ProcessArticleDTO
from app.repository.articleRepository import ArticleRepository
from app.repository.nerRepository import NerRepository


class ArticleService:
    def __init__(self, articleRepository: ArticleRepository, nerRepository: NerRepository):
        self.articleRepository = articleRepository
        self.nerRepository = nerRepository

    def getArticleByTitle(self, title: str):
        nodes = self.articleRepository.getByProperty('title', title)
        return nodes

    def getArticleById(self, id: int):
        node = self.articleRepository.getById(id)
        return node

    def processArticle(self, article: ProcessArticleDTO):
        if self.articleRepository.getByProperty('link', article.link):
            return
        node = self.articleRepository.save(
            {'title': article.title, 'description': article.description, 'image': article.image, 'link': article.link,
             'pubDate': article.pubDate})
        relationshipCategory = self.articleRepository.addRelation(node.id, 'Category', 'name', article.category,
                                                                  'IN_CATEGORY')
        relationshipLocation = self.articleRepository.addRelation(node.id, 'Location', 'name', article.location,
                                                                  'AT_LOCATION')
        return {'articleNode': node,
                'relationshipCategory': relationshipCategory,
                'relationshipLocation': relationshipLocation}
