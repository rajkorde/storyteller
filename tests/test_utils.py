import os
from tempfile import TemporaryDirectory

from src.core import Story, Student, StoryCondition
from src.utils import serialize, deserialize


def test_serialize_deserialize_roundtrip():
    story = Story(
        scenario_id="test-id",
        student=Student(interests="reading", age=10),
        condition=StoryCondition(situation="needs encouragement"),
    )

    with TemporaryDirectory() as tmpdir:
        file_path = os.path.join(tmpdir, "story.json")
        serialize(story, file_path)
        loaded = deserialize(file_path, Story)
        assert loaded == story

