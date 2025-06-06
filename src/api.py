from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uuid
import os

from cli import fill_in_details
from src.core import Story, Student, StoryCondition

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", include_in_schema=False)
def index() -> FileResponse:
    return FileResponse("static/index.html")


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


@app.get("/story/html/{scenario_id}", response_class=FileResponse)
def get_story_html(scenario_id: str) -> FileResponse:
    file_path = os.path.join("data", scenario_id, "story.html")
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Story not found")
    return FileResponse(file_path, media_type="text/html")
