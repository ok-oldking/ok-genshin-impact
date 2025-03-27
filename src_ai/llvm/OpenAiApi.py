import base64
import json
import pprint
import re

import cv2
from openai import OpenAI

from ok import Logger

logger = Logger.get_logger(__name__)

llvm_prompt = """
I'm writing an automated test for an app or game. I will provide you with the desired end goal and a screenshot of the app or game. Please respond with the all the actions to take (clicks or text input), as a list, formatted in json:
{
  "finished": false,
  "goal": "Describe what you want to achieve.",
  "actions":[
     { 
        "name": "describe what you are clicking", 
        "after_sleep_ms": 200, 
        "click": {"top_left_x": 0.112, "top_left_y": 0.233, "width": 0.013, "height": 0.051, "click_x": 0.113, "click_y": 0.241}
     },
     { "name": "describe what you are typing", "after_sleep_ms": 100, "input_text": "text to input"},
   ]
}
the top_left_x, top_left_y, width, height shows the ui element's position box, and the click_x, click_y shows where to click, the coordinates are relative percentages of the image's width and height in float, in precision of 3 digits after the decimal point.
and I will respond with a image after the actions, and give me the actions to take after that. If the end goal is achieved or can't be achieved, then respond with a json of:
{
  "finished": true,
  "error": "describe if there is a error"
}
"""

llvm_prompt = """
I'm writing an automated test for an app or game. I will provide you with the desired end goal and the current screenshot of the app or game.
Please respond with the all the actions to take (clicks or text input), as a list, formatted in json:
{
  "finished": false,
  "goal": "Describe what you want to achieve.",
  "actions":[
     { 
        "name": "describe what you are clicking", 
        "after_sleep_ms": 200, 
        "click": {"click_x": 0.113, "click_y": 0.241}
     },
     { "name": "describe what you are typing", "after_sleep_ms": 100, "input_text": "text to input"},
   ]
}
The click_x, click_y shows where to click, the coordinates are relative percentages of the image's width and height in float, in precision of 3 digits after the decimal point.
and I will respond with a image after the actions, and give me the actions to take after that. If the end goal is achieved or can't be achieved, then respond with a json of:
{
  "finished": true,
  "error": "describe if there is a error"
}
"""

llvm_prompt = """
You are a precise Android app automation agent that interacts with app through structured commands.
Your role is to:
1. Analyze the response histories from earlier responses, empty histories means it's the begging
2. Analyze the provided xml dump from uiautomator and optional screenshot from the current state of the app
3. Plan a sequence of actions to accomplish the given task
4. Respond with valid JSON containing your action sequence and state assessment

1. RESPONSE FORMAT: You must ALWAYS respond with valid JSON in this exact format:
   {
    "state": "Success|Failed|Done - Done if the end goal is achieved, Error if then end goal can't be achieved or encountered an error, Success if you can successfully provide the actions",
    "error": "describe if there is a error",
    "goal": "What needs to be done with the next actions"
    "actions": [
       {
         "action": "click",
         "description": "click the login button",
         // action-specific parameters
       },
       // ... more actions in sequence
    ]
   }

2. ACTIONS: You can specify multiple actions to be executed in sequence.
   The supported actions are: "click", "input_text", "scroll"
   All the locations need to be calculated base on the xml uiautomator dump
   example of a login action sequence:
   [
       {"action": "click", "description": "click the username input", "x": 100, "y": 200},
       {"action": "input_text", "description": "input the text abc as username", "text": "abc"},
       {"action": "click", "description": "click password area",  "x": 100, "y": 300},
       {"action": "input_text", "description": "input text 123 as password ", "text": "123"}, // 
       {"action": "click", "click the login button", "x": 200, "y": 400}, // click the login button
   ]
   the scroll actions are in the format of, indicating the starting mouse point to the end mouse point:
   {"action": "scroll", description: "scroll down to the next list", "from_x": 100, "from_y": 400, "to_x": 100, "to_y": 300}
   the wait actions means the page is loading, and the user need to wait for the page to change, at least wait 2000 milliseconds, and wait more if the page does change from last time:
   {"action": "wait", description: "wait for the login to complete", "milliseconds": 2000}
   the back action sends the back key to the android app
   {"action": "back", description: "send back to the android app"}

3. NAVIGATION & ERROR HANDLING:
   - If stuck, try alternative approaches
   - Handle popups by accepting or closing them
   - Use scroll to find elements you are looking for

4. TASK COMPLETION:
   - set the evaluation_previous_goal to Done and return a empty actions as soon as the task is complete
   - Don't hallucinate actions

5. VISUAL CONTEXT:
   - When an image is provided, use it to understand the layout

6. ACTION SEQUENCING:
   - Actions are executed in the order they appear in the list
   - Each action should logically follow from the previous one
   - If the page changes after an action, the sequence is interrupted and you get the new state.
   - If content only disappears the sequence continues.
   - Only provide the action sequence until you think the page will change.
   - Try to be efficient, e.g. fill forms at once, or chain actions where nothing changes on the page like saving, extracting, checkboxes...
   - only use multiple actions if it makes sense.
   - use maximum 20 actions per sequence

Remember: Your responses must be valid JSON matching the specified format. Each action in the sequence must be valid.
"""


class OpenAiApi:
    def __init__(self, api_key, model='gpt-4o-mini', url="https://chatapi.littlewheat.com/v1", prompt=None):
        self.api_key = api_key
        self.model = model
        self.client = OpenAI(
            api_key=api_key,  # This is the default and can be omitted
            base_url=url,
        )
        self.prompt = prompt

    def _encode_image(self, image):
        _, buffer = cv2.imencode('.png', image)
        jpg_base64 = base64.b64encode(buffer).decode('utf-8')
        return jpg_base64

    def converse(self, user_messages, image=None, step=1):
        messages = [{"role": "system", "content": llvm_prompt}]
        user_contents = []
        for user_message in user_messages:
            user_contents.append({"type": "text", "text": user_message})

        if image is not None:
            img_b64_str = self._encode_image(image)
            img_type = "image/png"
            user_contents.append(
                {"type": "image_url", "image_url": {"url": f"data:{img_type};base64,{img_b64_str}"}},
            )

        messages.append({"role": "user",
                         "content": user_contents})
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0,
            response_format={"type": "json_object"},
        )
        input_tokens = response.usage.prompt_tokens
        output_tokens = response.usage.completion_tokens
        logger.info('Message response: {}'.format(response.choices[0].message.content))
        return parse_json_from_string(response.choices[0].message.content), input_tokens, output_tokens


def parse_json_from_string(json_string):
    json_string = re.sub(r"```json\n?", "", json_string)
    json_string = re.sub(r"```", "", json_string)
    json_string = json_string.strip()

    try:
        data = json.loads(json_string)
        return data
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON: {e}")
        return None


if __name__ == "__main__":
    api_key = "sk-XO2tn9Rb0hnl2OjeW4lHZTqAERnlvMs93HhpPqwmdDbUuvZb"
    if not api_key:
        raise ValueError("No OPENAI_API_KEY environment variable set")

    openai_api = OpenAiApi(api_key, model='gpt-4o-latest')

    try:
        image_path = "tests/images/delete_from_channel.png"
        image = cv2.imread(image_path)
        if image is not None:
            response = openai_api.converse("我要从这个频道中选中并移除所有用户", image=image)
            print(f"OpenAI (with image1):")
            pprint.pprint(response)
        else:
            print(f"Could not read image from {image_path}")
    except FileNotFoundError:
        print("Image file not found. Skipping image example.")

    # try:
    #     image_path = "tests/images/delete_from_channel2.png"
    #     image = cv2.imread(image_path)
    #     if image is not None:
    #         response = openai_api.converse("This is what I got after the actions:", image=image)
    #         print(f"OpenAI (with image2):")
    #         pprint.pprint(response)
    #     else:
    #         print(f"Could not read image from {image_path}")
    # except FileNotFoundError:
    #     print("Image file not found. Skipping image example.")
