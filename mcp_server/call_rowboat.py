import requests
from rowboat.client import Client
from rowboat.schema import UserMessage


PROJECT_ID = "<PROJECT_ID>"
API_KEY = "<API_KEY>"

client = Client(
    host="http://localhost:3000",
    projectId=PROJECT_ID,
    apiKey=API_KEY,
)


def use_requests_api(user_input: str):
    url = f"http://localhost:3000/api/v1/{PROJECT_ID}/chat"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    request_json = {
        "messages": [
            {"role": "user", "content": user_input},
        ],
        "state": None,
    }

    response = requests.post(url, headers=headers, json=request_json)
    resp_json = response.json()

    response_str = resp_json["turn"]["output"][-1]["content"]
    return response_str


def use_rowboat_sdk(user_input: str):
    result = client.run_turn(
        messages=[UserMessage(role='user', content=user_input)],
    )
    response_str = result.turn.output[-1].content
    return response_str


if __name__ == "__main__":
    user_input = "What will the weather be in Rajkot tomorrow?"

    using_requests_api = use_requests_api(user_input=user_input)
    print(f"Using requests API call: {using_requests_api}")

    using_rowboat_sdk = use_rowboat_sdk(user_input=user_input)
    print(f"Using Rowboat SDK: {using_rowboat_sdk}")
