from flask import Flask, request
from naoqi import ALProxy

app = Flask(__name__)
speech_proxy = ALProxy("ALTextToSpeech", "192.168.0.192", 9559)
speech_proxy.setLanguage("marathi")  # Update the language code to 'marathi'


@app.route('/say', methods=['GET'])
def say_something():
    message = "तुम्ही कसे आहात?"
    data = request.args.to_dict()
    speech_proxy.say(str(data['message']))
    return 'OK'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8891)