from flask import Flask, request, jsonify, redirect
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)


@app.route('/whatsapp', methods=['GET', 'POST'])
def whatsapp_reply():
    response = MessagingResponse()
    response.message('It works')

    return str(response)

if __name__ == '__main__':
    app.run(port=8080)
