from flask import Flask, request, jsonify
from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import os

app = Flask(__name__)

# Watson credentials from environment variables
api_key = os.getenv("7zLgxDJgTn-lKvodDO2sT9ZN4t7hYzPckl6G0pwBjSNB")
url = os.getenv("https://api.au-syd.assistant.watson.cloud.ibm.com/instances/a87f2d76-6752-42b1-a9ab-fd0d71df8a55")
assistant_id = os.getenv("566d4c72-9802-42a1-95ab-f215822b8d08")

authenticator = IAMAuthenticator(api_key)
assistant = AssistantV2(
    version='2023-09-26',
    authenticator=authenticator
)
assistant.set_service_url(url)

# Create a session once
session_id = assistant.create_session(assistant_id=assistant_id).get_result()['session_id']

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    response = assistant.message(
        assistant_id=assistant_id,
        session_id=session_id,
        input={'text': user_message}
    ).get_result()

    bot_reply = "I didn't understand that."
    if response['output']['generic']:
        bot_reply = response['output']['generic'][0]['text']

    return jsonify({"reply": bot_reply})

@app.route("/", methods=["GET"])
def home():
    return "BookBot is running ✅"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
