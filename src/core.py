from pydantic import BaseModel, Field


class Student(BaseModel):
    name: str
    interests: str
    age: int


class StoryCondition(BaseModel):
    situation: str
    guidance: str | None = None


class Story(BaseModel):
    scenario_id: str
    student: Student
    condition: StoryCondition
    setting: str = ""
    story_text: str = ""

    characters: list[str] = Field(default_factory=list)
    key_events: list[str] = Field(default_factory=list)
    STORY_LIMIT: int = 250
