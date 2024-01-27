from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import requests
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import requests
import openai

app = FastAPI()

# Enable CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rasa server endpoint
rasa_endpoint = "http://localhost:5005/webhooks/rest/webhook"  # Update with your Rasa server's URL


@app.post("/predict")
async def predict(data: dict):
    # Get user input message
    message = data.get('message', '')

    # Make a request to the Rasa server's REST endpoint
    rasa_response = requests.post(rasa_endpoint, json={"message": message})

    # Extract the response text from the Rasa server's response
    rasa_response_json = rasa_response.json()

    # Extract and concatenate all text messages from the response
    response_text = "\n".join(msg.get("text", "") for msg in rasa_response_json)

    # Return the concatenated response text
    return JSONResponse(content={"response": response_text})


import openai

# OpenAI API key
openai.api_key = ''  # Update with your OpenAI API key


@app.post("/format_flow")
async def format_flow(data: dict):
    try:
        # Get user input message
        message = data.get('message', '')

        # Make a request to the Rasa server's REST endpoint
        rasa_response = requests.post(rasa_endpoint, json={"message": message})
        formatted_flow = {
            "nodes": [
                {"id": "1", "type": "task", "data": {"label": "Define the project"}, "position": {"x": 100, "y": 100}},
                {"id": "2", "type": "task", "data": {"label": "Set up a Vercel account"},
                 "position": {"x": 300, "y": 100}},
                # Add more nodes as needed
            ],
            "edges": [
                {"id": "e1", "source": "1", "target": "2"},
                # Add more edges as needed
            ]
        }
        # Extract the response text from the Rasa server's response
        rasa_response_json = rasa_response.json()
        prompt="Please format the input data in a JSON structure that can be used with React Flow. Ensure that tasks, subtasks, and links are appropriately represented for visualization."
        # Extract and concatenate all text messages from the Rasa response
        rasa_text = "\n".join(msg.get("text", "") for msg in rasa_response_json)
        print(rasa_text)
        combined_input = f"Please format this data  in a JSON structure that can be used with React Flow like that {formatted_flow}. Ensure that tasks, subtasks, and links are appropriately represented for visualization also return your responce only json in that fromat  that will be used to visualize  this  tasks in reactflow  here si the data.\n{rasa_text}"
        print('/////////////////////////////////')
        print(combined_input)

        # Use OpenAI to generate a JSON representation
        response = openai.Completion.create(
            engine="gpt-3.5-turbo-instruct",
            prompt=combined_input,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )

        # Extract the JSON representation from the OpenAI response
        generated_json = response.choices[0].text

        json_start_index = generated_json.find('{\n  \"nodes')

        if json_start_index != -1:
            # Extract the relevant JSON portion
            generated_json = generated_json[json_start_index:]
        else:
            raise ValueError("JSON data not found in OpenAI response")

        # Return the formatted JSON
        return JSONResponse(content={"formatted_flow": generated_json})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))