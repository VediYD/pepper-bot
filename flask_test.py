from flask import Flask, request
from naoqi import ALProxy

app = Flask(__name__)
speech_proxy = ALProxy("ALTextToSpeech", "192.168.0.192", 9559)


@app.route('/say', methods=['POST'])
def say_something():
    #message = "Testing"
    data = request.form.to_dict()
    speech_proxy.say(str(data['message']))
    return 'OK'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8891)
    
