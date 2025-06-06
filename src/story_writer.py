from agents import Agent, ModelSettings, Runner
import asyncio

from src.core import Story

story_writer_prompt = f"""
You are a storyteller who can create wondrous and appealing stories for children dealing with special needs. You will be provided a specific situation a child is facing and your job is write a short story to help the child deal with the situation along with a parent or teacher.

* The story should be engaging and interesting for the child.
* All main characters should have a name and a distinct personality. Also, their species should be mentioned in the story (eg Leo the painter, Max the mouse etc)
* The story should be age appropriate based on the child's age mentioned below.
* If possible, the story should be based on the child's interests mentioned below. It's not mandatory, so don't force it.
* If some guidance is provided, the story should be based on that guidance.
* The story should be set in a single location and should not have any travel or movement.
* The story should have 2-3 characters only
* The story should be short and sweet, with around {Story.STORY_LIMIT} words.

"""


story_writer_agent = Agent(
    name="storyteller",
    model="gpt-4o-mini",
    model_settings=ModelSettings(temperature=0.8),
    instructions=story_writer_prompt,
)


def create_story(story: Story) -> str:
    print("Creating Story...")
    input = f"""
    Situation: {story.condition.situation}, 
    Age: {story.student.age}, 
    Interests: {story.student.interests}, 
    Guidance: {story.condition.guidance}"""

    result = asyncio.run(
        Runner.run(
            story_writer_agent,
            input=input,
        )
    )

    return (
        result.final_output
        if result.new_items[0].raw_item.status == "completed"
        else ""
    )
