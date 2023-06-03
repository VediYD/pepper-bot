from flask import Flask, request
from naoqi import ALProxy
import time

app = Flask(__name__)
# Bot's IP address
ip = "192.168.0.192"
port = 9559
speech_proxy = ALProxy("ALTextToSpeech", ip, port)
speech_recognition_proxy = ALProxy("ALSpeechRecognition", ip, port)
memory_proxy = ALProxy("ALMemory", ip, port)


@app.route('/say', methods=['POST'])
def say_something():
    data = request.form.to_dict()
    speech_proxy.say(str(data['message']))
    return 'OK'

@app.route('/listen', methods=['POST'])
def listen():
    pass


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8891)