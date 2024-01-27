# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

import os
import openai
import random
import requests
import pandas as pd
from rasa_sdk import Action, Tracker
from typing import Any, Text, Dict, List
from rasa_sdk.executor import CollectingDispatcher
# This is a simple example for a custom action which utters "Hello World!"
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import openai
def get_answers_from_chatgpt(user_text):

    # OpenAI API Key
    openai.api_key = os.getenv("GPT_API_KEY")

    # Use OpenAI API to get the response for the given user text and intent
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt= user_text,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    ).choices[0].text

    # Return the response from OpenAI
    return response
# from typing import Any, Text, Dict, List
#
class CreatePlanAction(Action):
    def name(self):
        return "action_create_plan"

    def run(self, dispatcher, tracker, domain):
        user_input = tracker.latest_message.get('text')

        # Use OpenAI to generate a planning response based on the user input
        openai.api_key = ''
        prompt = f"Create a plan for the project: {user_input}"
        response = openai.Completion.create(
            engine="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=300,  # Adjust based on your requirements
            n=1,
            stop=None
        )

        # Extract the generated response from OpenAI
        generated_response = response['choices'][0]['text']

        # Respond to the user with the OpenAI-generated planning details
        dispatcher.utter_message(text=generated_response)

        return []




# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
