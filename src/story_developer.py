from agents import Agent, ModelSettings, Runner

from src.core import Story, StoryCharacteristics

story_developer_prompt = """
You are a story developer who can read a short story created for children and extract and expand on the following story elements:

* Setting - describe the setting of the story with delightful but concise details. This will help the image creator create a beautiful image for the story.
* Characters - create a list of the main characters of the story. For each character, you add in delightful details that would strike the fancy of the child and help the image creator to create vivid images of the characters that would accompany the story text.
* Key Events - Extract 2-4 main events from the story and add very brief detail to the event, so that its clear what part of the story the event is refering to. The events should be in the order they occur in the story.

"""


story_developer_agent = Agent(
    name="storyteller",
    model="gpt-4o-mini",
    model_settings=ModelSettings(temperature=0.8),
    instructions=story_developer_prompt,
    output_type=StoryCharacteristics,
)


def create_details(story: Story) -> StoryCharacteristics:
    result = Runner.run_sync(story_developer_agent, input=story.story_text)

    if result.new_items[0].raw_item.status != "completed" or not isinstance(
        result.final_output, StoryCharacteristics
    ):
        raise RuntimeError("Failed to create story details")

    return result.final_output
