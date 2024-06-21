from flask import Flask, request, jsonify, redirect
from twilio.twiml.messaging_response import MessagingResponse
from textSpeech.convert import Convert

# ngrok http --domain=martin-polished-remarkably.ngrok-free.app 8080
app = Flask(__name__)


@app.route('/whatsapp', methods=['GET', 'POST'])
def whatsapp_reply():
    conversor = Convert()
    try:
        data = request.form.to_dict()
    except Exception as e:
        print(e)
    print(data)
    query = data['Body']
    sender_id = data['From']
    print(sender_id)
    print(query)
    print(f'Sender id - {sender_id}')
    # get the user
    # if not create
    # create chat_history from the previous conversations
    # question and answer
    if 'MediaUrl0' in data.keys():
        print(data['MediaUrl0'])
        #audio_test = conversor.speech_to_text(data['MediaUrl0'])
        #print(audio_test)
    return 'OK', 200
#         transcript = transcript_audio(data['MediaUrl0'])
#         if transcript['status'] == 1:
#             print(f'Query - {transcript["transcript"]}')
#             response = chat_completion(transcript['transcript'])
#         else:
#             response = config.ERROR_MESSAGE
#     else:
#         print(f'Query - {query}')
#         response = chat_completion(query)
#     print(f'Response - {response}')
#     send_message(sender_id, response)
#     print('Message sent.')

if __name__ == '__main__':
    app.run(port=8080)
