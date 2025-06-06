import asyncio
import uuid

import typer
from dotenv import load_dotenv
from loguru import logger
from rich.prompt import IntPrompt, Prompt

from src.core import Story, StoryCondition, Student
from src.feature_flags import FeatureFlags
from src.image_creator import ImageCreator
from src.photographer import SceneDescription, create_scene_descriptions
from src.publisher import publish_html
from src.screenplay_writer import create_screenplay
from src.story_writer import create_story
from src.utils import deserialize, serialize

assert load_dotenv()

__version__ = "0.0.1"

app = typer.Typer()
flags = FeatureFlags.read_feature_flags()


def fill_in_details(story: Story):
    # create story
    story_id = story.scenario_id

    if flags.create_story:
        story_text = create_story(story)
        if story_text:
            story.story_text = story_text
            serialize(story, f"data/{story_id}/story.json")
    else:
        story_text = story.story_text

    if not story_text:
        logger.error("Failed to create story")
        raise typer.Exit(1)

    # create screenplay
    if flags.create_screenplay:
        details = create_screenplay(story)
        if details:
            story.characteristics = details
            serialize(story, f"data/{story_id}/story.json")
    else:
        details = story.characteristics

    if not details:
        logger.error("Failed to create screenplay")
        raise typer.Exit(1)

    # create image descriptions
    if flags.create_scene_descriptions:
        scene_descriptions = create_scene_descriptions(story)
        if scene_descriptions and scene_descriptions.descriptions:
            story.key_events_details = scene_descriptions.descriptions
            serialize(story, f"data/{story_id}/story.json")
    else:
        scene_descriptions = SceneDescription()
    scene_descriptions.descriptions = story.key_events_details

    if not scene_descriptions or not scene_descriptions.descriptions:
        logger.error("Failed to create scene descriptions")
        raise typer.Exit(1)

    # create images
    if flags.create_images:
        image_creator = ImageCreator(story)
        asyncio.run(image_creator.create_character_sheet())
        asyncio.run(image_creator.create_scene_images())

    # Publish

    if flags.publish:
        publish_html(story=story)


def version_callback(value: bool):
    if value:
        print(f"Recipe-Items  CLI Version: {__version__}")
        raise typer.Exit()


def print_header():
    typer.secho("\n-----------------------", fg=typer.colors.GREEN, bold=True)
    typer.secho("Welcome to Storyteller!", fg=typer.colors.GREEN, bold=True)
    typer.secho("-----------------------\n", fg=typer.colors.GREEN, bold=True)


# get student info
def ask_student_questions() -> dict[str, str | int]:
    answers: dict[str, str | int] = {}
    try:
        answers["age"] = IntPrompt.ask("What is their age?")
        answers["situation"] = Prompt.ask(
            "What is student situation that needs correcting?"
        )
        answers["interests"] = Prompt.ask("What are their interests or hobbies?")

        answers["guidance"] = Prompt.ask(
            "Any guidance for the story (eg use forest setting, use bright colors etc)? Hit enter for none"
        )
    except Exception as e:
        typer.secho(f"Error during input: {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)
    return answers


@app.command()
def get_student_info(scenario_id: str | None = typer.Argument(None)):
    if flags.get_user_input:
        print_header()
        responses = ask_student_questions()

        assert isinstance(responses["interests"], str)
        assert isinstance(responses["age"], int)

        scenario_id = str(uuid.uuid4())
        print(f"Scenario ID created: {scenario_id}")
        student = Student(
            interests=responses["interests"],
            age=responses["age"],
        )

        assert isinstance(responses["situation"], str)
        assert responses["guidance"] is None or isinstance(responses["guidance"], str)
        guidance = None if not responses["guidance"] else responses["guidance"]
        story_condition = StoryCondition(
            situation=responses["situation"],
            guidance=guidance,
        )

        story = Story(
            scenario_id=scenario_id,
            student=student,
            condition=story_condition,
        )

        if flags.save_data:
            serialize(story, f"data/{scenario_id}/story.json")

    else:
        if not scenario_id:
            print(
                "You must provide a scenario id if feature flag for getting user input is off."
            )
            raise typer.Exit(code=1)
        try:
            story = deserialize(
                f"data/{scenario_id}/story.json",
                Story,
            )
        except RuntimeError:
            print(f"Invalid scenario id: {scenario_id}")
            raise typer.Exit(code=1)

    # print(f"{story=}")

    fill_in_details(story)


if __name__ == "__main__":
    app()
