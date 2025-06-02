from agents import Agent, ModelSettings, Runner

from src.core import Story

publisher_prompt = """
I have a children's story and few images that illustrate different scenes from the story. Generate an HTML page that would present the story as a fun kid friendly story that parents can read to their children. The story should be formatted in a way that it is easy to read and understand. The images should be placed in their own newline right AFTER the text of the scene they depict. 

You will be provided the story and list of image url and scene descriptions of the scene they represent.

The image tags for the scence should be placed right AFTER the relevent story section it represents on a new line.
Use colorful font for title only.
Use larger font size for the story. Something that is appropriate for kids.
Use clear, readable formatting.
The story should only be in the middle demarcated section with white gutters (about 50% of the port width). 
All images should be resized to 40% of their size.
Use child friendly colors and fonts.
But dont use comic sans.
The text should be left justified.
The image tags should be center justified.

Do not add extra commentary or explanation.

Output only the HTML code and nothing else. No indicators like triple quotes
"""

publisher_agent = Agent(
    name="publisher",
    model="gpt-4o-mini",
    model_settings=ModelSettings(temperature=0.8),
    instructions=publisher_prompt,
)


def publish_html(story: Story):
    print("Publishing HTML...")
    input = f"STORY\n{story.story_text}\n"

    for i, scene in enumerate(story.characteristics.key_events):
        scene_id = i + 1
        url = f"images/scene_{scene_id}.png"
        input += f"Scene {scene_id}: {scene}\n"
        input += f"Image URL: {url}\n\n"

    result = Runner.run_sync(publisher_agent, input=input)

    if result.new_items[0].raw_item.status != "completed" or not isinstance(
        result.final_output, str
    ):
        raise RuntimeError("Failed to create HTML")

    html = result.final_output
    html = html.replace("```html", "").replace("```", "")

    with open(f"data/{story.scenario_id}/story.html", "w") as f:
        f.write(html)
