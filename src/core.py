from typing import ClassVar

from pydantic import BaseModel, Field


class Student(BaseModel):
    interests: str
    age: int


class StoryCondition(BaseModel):
    situation: str
    guidance: str | None = None


class Character(BaseModel):
    name: str
    description: str


class StoryCharacteristics(BaseModel):
    story_setting: str
    characters: list[Character]
    key_events: list[str]


class Story(BaseModel):
    STORY_LIMIT: ClassVar[int] = 250

    scenario_id: str
    student: Student
    condition: StoryCondition
    story_text: str = ""

    characteristics: StoryCharacteristics | None = None
    key_events_details: list[str] = Field(default_factory=list)
