import base64
from pathlib import Path

from openai import OpenAI
from openai.types.responses.response import Response
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)

from src.core import Story


class ImageCreator:
    character_sheet_creator_prompt = """
You are an expert in creating images for children's books. You will be provided with a children's story, the setting of the story and a list of characters in the story. Your job is to create an character sheet image that contain the characters in the setting provided. The character sheet image would be used as a reference to create consistent characters in creating for various scenes of the story.

* Do NOT include any text in the image.
* Each character shot should be a full body shot.
* The sheet should be a single image, but include shots of the characters in front and side profile.
* The shots of same character should be consistent in every way.
* The characters should be in the setting provided.
"""

    image_generator_prompt = """
You are an expert in creating appealing images for children's books. You will be provided with a story, the setting of the story and a description of a scene from the story. You will also be provided with a character sheet image that contain the depictions of the characters in the setting of the story. Your job is to create a playful image for the scene description that would be part of the story book. You must the characters in the scene consistent with the characters in the character sheet image.

* Do not include any text in the image.
* Pay attention to small nuances (eg if the character in the character sheet is wearing a cap, make sure the cap is present in the scene as well). Not following consistency rule with break the continuity of the story.
"""

    def __init__(self, story: Story):
        self.story = story
        self.client = OpenAI()
        self.character_sheet_response_id: str | None = None

    @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(3))
    def _image_completion_with_backoff(
        self,
        prompt: str,
        input: str,
        previous_id: str | None = None,
        quality: str = "medium",
    ) -> Response:
        response = self.client.responses.create(
            model="gpt-4o-mini",
            instructions=prompt,
            previous_response_id=previous_id,
            input=input,
            tools=[
                {
                    "type": "image_generation",
                    "quality": quality,
                    "size": "1024x1024",
                }
            ],
        )
        return response

    def create_character_sheet(self):
        print("Generating character sheet")

        input = f"""
        Story: {self.story.story_text}, \n\n 
        Setting: {self.story.characteristics.story_setting}, \n\n
        Characters: {self.story.characteristics.characters}, \n\n
        """

        character_sheet_response = self._image_completion_with_backoff(
            ImageCreator.character_sheet_creator_prompt, input, quality="high"
        )
        self.character_sheet_response_id = character_sheet_response.id

        sheet_image_data = [
            output.result
            for output in character_sheet_response.output
            if output.type == "image_generation_call"
        ]

        image_path = f"data/{self.story.scenario_id}"
        Path(image_path).mkdir(parents=True, exist_ok=True)
        if sheet_image_data:
            image_base64 = sheet_image_data[0]

            with open(f"{image_path}/character_sheet.png", "wb") as f:
                f.write(base64.b64decode(image_base64))

    def create_scene_images(self):
        assert self.character_sheet_response_id, (
            "Must create character sheet before creating scene images"
        )
        for i, scene_description in enumerate(self.story.key_events_details):
            print(f"Generating scene {i + 1}")

            input = f"""
            Story: {self.story.story_text}, \n\n 
            Setting: {self.story.characteristics.story_setting}, \n\n
            Scene Description: {scene_description}, \n\n
            """

            response = self._image_completion_with_backoff(
                ImageCreator.image_generator_prompt,
                input,
                self.character_sheet_response_id,
            )

            image_data = [
                output.result
                for output in response.output
                if output.type == "image_generation_call"
            ]

            image_path = f"data/{self.story.scenario_id}/images"
            Path(image_path).mkdir(parents=True, exist_ok=True)

            if image_data:
                image_base64 = image_data[0]

                with open(
                    f"data/{self.story.scenario_id}/images/scene_{i + 1}.png", "wb"
                ) as f:
                    f.write(base64.b64decode(image_base64))
