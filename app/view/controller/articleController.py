from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, status

from app.containers import Container
from app.domain.articleService import ArticleService
from app.domain.dto.processArticleDTO import ProcessArticleDTO
from app.view.request.processArticleRequest import ProcessArticleRequest

router = APIRouter()


@router.post('/process')
@inject
async def process(articleRequest: ProcessArticleRequest,
                  articleService: ArticleService = Depends(Provide[Container.articleService])):
    print('in route')
    articleNode = articleService.processArticle(ProcessArticleDTO(title=articleRequest.title,
                                                                  location=articleRequest.location,
                                                                  description=articleRequest.description,
                                                                  image=articleRequest.image,
                                                                  category=articleRequest.category,
                                                                  link=articleRequest.link,
                                                                  pubDate=articleRequest.pubDate
                                                                  ))
    return articleNode


@router.get('/{id}')
@inject
async def getById(id: int,
                  articleService: ArticleService = Depends(Provide[Container.articleService])):
    article = articleService.getArticleById(id)
    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return article


@router.get('/title/{title}')
@inject
async def getAll(title: str,
                 articleService: ArticleService = Depends(Provide[Container.articleService])):
    nodes = articleService.getArticleByTitle(title)
    return nodes
