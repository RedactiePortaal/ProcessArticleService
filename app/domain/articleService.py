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
        relationshipCategory = self.articleRepository.addRelationOutgoing(node.id, 'Category', 'name', article.category,
                                                                          'IN_CATEGORY')
        relationshipLocation = self.articleRepository.addRelationOutgoing(node.id, 'Location', 'name', article.location,
                                                                          'AT_LOCATION')
        namedEntities = self.nerRepository.getNamedEntities(article.title + ". " + article.description)
        if not namedEntities:
            return {'articleNode': node,
                    'relationshipCategory': relationshipCategory,
                    'relationshipLocation': relationshipLocation}
        for sentence in namedEntities:
            for index, ent in enumerate(sentence):
                relationship = self.articleRepository.addRelationIncoming(node.id, ent.type, 'name', ent.name,
                                                                          "IN_ARTICLE")
                ent.id = relationship.target.id

        for sentence in namedEntities:
            for index, ent in enumerate(sentence):
                entsWithoutCurrent = sentence.copy()
                entsWithoutCurrent.pop(index)
                for otherEnt in entsWithoutCurrent:
                    self.articleRepository.connectNodesById(ent.id, otherEnt.id, "MENTIONED_TOGETHER")
        return {'articleNode': node,
                'relationshipCategory': relationshipCategory,
                'relationshipLocation': relationshipLocation,
                'entities': namedEntities}
