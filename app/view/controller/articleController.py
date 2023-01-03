from fastapi import APIRouter

from app.view.request.processArticleRequest import ProcessArticleRequest
from app.view.viewModel.processArticleResponse import ProcessArticleResponse

router = APIRouter()


@router.post('/process', response_model=ProcessArticleResponse)
async def process(articleRequest: ProcessArticleRequest):
    return ProcessArticleResponse()
