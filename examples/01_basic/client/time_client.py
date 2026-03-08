# library to create a unique identifier for each task
import uuid

# library for making HTTP requests to communicate with the agent
import requests

# ---------------------------------------
# Step 1 – Discover the Agent
# ---------------------------------------

# base URL where the server agent
base_url = "http://127.0.0.1:8000"

# use HTTP GET to fetch the agent's card from the well-known discovery endpoint
res = requests.get(f"{base_url}/.well-known/agent.json")

# if the request fails (not status code 200), raise an error
if res.status_code != 200:
    raise Exception("Failed to discover agent.")

# parse the response JSON into a Python dictionary
agent_info = res.json()

# display some basic info about the discovered agent
print(f"Connected to: {agent_info['name']} - {agent_info['description']}")

# ---------------------------------------
# Step 2 – Prepare a Task
# ---------------------------------------

# generate a unique ID for this task using uuid4 (random UUID)
task_id = str(uuid.uuid4())

# construct the A2A task payload as a Python dictionary
# According to A2A spec, we need to include:
# - "id": the unique task ID
# - "message": an object with "role": "user" and a list of "parts" (in this case, text only)
task_payload = {
    "id": task_id,
    "message": {
        "role": "user",  # indicates that the message is coming from the user
        "parts": [
            {"text": "What time is it?"}  # this is the question the user is asking
        ],
    },
}

# ---------------------------------------
# Step 3 – Send the Task to the Agent
# ---------------------------------------

# send an HTTP POST request to the /tasks/send endpoint of the agent
response = requests.post(
    f"{base_url}/tasks/send",
    json=task_payload,  # requests will serialize our dictionary as JSON
)

# if the server didn’t return a 200 OK status, raise an error
if response.status_code != 200:
    raise Exception(f"Task failed: {response.text}")

# parse the agent's JSON response into a Python dictionary
response_data = response.json()

# ---------------------------------------
# Step 4 – Display the Agent's Response
# ---------------------------------------

# extract the list of messages returned in the response
# this typically includes both the user's message and the agent's reply
messages = response_data.get("messages", [])

# if there are messages, extract and print the last one (agent’s response)
if messages:
    final_reply = messages[-1]["parts"][0]["text"]
    print("Agent says:", final_reply)
else:
    # If no messages were received, notify the user.
    print("No response received.")


# ---------------------------------------
# Run with: uv run filename
# ---------------------------------------
