from dependency_injector.wiring import Provide
from fastapi import APIRouter, Depends

from app.containers import Container
from app.domain.articleService import ArticleService
from app.view.request.processArticleRequest import ProcessArticleRequest
from app.view.viewModel.processArticleResponse import ProcessArticleResponse

router = APIRouter()


@router.post('/process', response_model=ProcessArticleResponse)
async def process(articleRequest: ProcessArticleRequest,
                  articleService: ArticleService = Depends(Provide[Container.articleService])):
    articleService.getArticleByTitle(articleRequest.title)
    return ProcessArticleResponse()
