from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid

from cli import fill_in_details
from src.core import Story, Student, StoryCondition

app = FastAPI()


class StoryRequest(BaseModel):
    age: int
    interests: str
    situation: str
    guidance: str | None = None


@app.post("/story", response_model=Story)
def create_story(request: StoryRequest) -> Story:
    scenario_id = str(uuid.uuid4())
    student = Student(interests=request.interests, age=request.age)
    condition = StoryCondition(situation=request.situation, guidance=request.guidance)

    story = Story(
        scenario_id=scenario_id,
        student=student,
        condition=condition,
    )

    try:
        fill_in_details(story)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return story
