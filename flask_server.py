!pip install speechrecognition==3.8.1
from flask import Flask, request, jsonify
from naoqi import ALProxy
import time
import speech_recognition as sr

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

def convert_wav_to_text(audio_path):
    r = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio_data = r.record(source)
    try:
        text = r.recognize_google(audio_data)
        return text
    except sr.UnknownValueError:
        return "Speech recognition could not understand audio"
    except sr.RequestError as e:
        return "Could not request results from Google Speech Recognition service: " + str(e)
    except Exception as e:
        return "An error occurred during speech recognition: " + str(e)


@app.route('/convert', methods=['POST'])
def convert_audio():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'})

    audio_file = request.files['file']
    if audio_file.filename == '':
        return jsonify({'error': 'No file selected'})

    # Save the uploaded file
    audio_path = 'recordings/' + audio_file.filename
    audio_file.save(audio_path)

    # Convert audio to text
    result = convert_wav_to_text(audio_path)

    # Return the converted text
    return jsonify({'text': result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8891)