from flask import Flask, request, jsonify
import speech_recognition as sr

app = Flask(__name__)

import speech_recognition as sr

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
    app.run(debug=True)
