from typing import Annotated
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from ml_service.mcqa_model import MCQA_MODEL


ROUTER = APIRouter()


class MCQARequest(BaseModel):
    text: str
    choice1: str
    choice2: str
    choice3: str
    choice4: str

class MCQAResponse(BaseModel):
    chosen_label: str
    confidence: float



#mcqa model - post
@ROUTER.post("/mcqa", response_model=MCQAResponse)
async def mcqa(params: Annotated[MCQARequest, Depends()]) -> MCQAResponse:
    text_with_blank = params.text
    choices = [params.choice1, params.choice2, params.choice3, params.choice4]

    best_choice, confidence = MCQA_MODEL.predict(text_with_blank, choices)

    return MCQAResponse(chosen_label=best_choice, confidence=confidence)



