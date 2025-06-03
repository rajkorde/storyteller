from agents import Agent, ModelSettings, Runner
from pydantic import BaseModel, Field

from src.core import Story

photographer_prompt = """
You are the director of photography whose job is to create description of how a scene from a story would look like. You will be provided a children's story, the story setting, characters and key events of the story. Your job is decide the shot composition, lighting, camera angle and other details to create a beautiful image for each scene. This descriptions will later be passed on to an image creator to create the images.

* Return the same number of descriptions as there are key events in the story.
* You dont need to include all the characters of the story in each scene. Pick the relevant ones only.
* Do not describe the setting again in the shot description. Just focus on shot composition, lighting, camera angle and other details.
* The shot descriptions should be cohesive throughout the story. So you cannot have evening shot in one scene and morning shot in another.
* Include all details needed for a image generator to create images that would be appealing to children.
"""


class SceneDescription(BaseModel):
    descriptions: list[str] = Field(default_factory=list)


photographer_agent = Agent(
    name="photographer",
    model="gpt-4o-mini",
    model_settings=ModelSettings(temperature=0.8),
    instructions=photographer_prompt,
    output_type=SceneDescription,
)


def create_scene_descriptions(story: Story) -> SceneDescription:
    print("Creating Scene descriptions...")
    input = f"""
    Story: {story.story_text}, \n\n
    Setting: {story.characteristics.story_setting}, \n\n
    Characters: {story.characteristics.characters}, \n\n
    Key Events: {story.characteristics.key_events}"""

    result = Runner.run_sync(photographer_agent, input=input)

    if result.new_items[0].raw_item.status != "completed" or not isinstance(
        result.final_output, SceneDescription
    ):
        raise RuntimeError("Failed to create scene descriptions")

    return result.final_output
