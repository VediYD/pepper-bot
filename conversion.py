from flask import Flask, request, jsonify
import speech_recognition as sr

app = Flask(__name__)

def convert_wav_to_text(audio_path):
    r = sr.Recognizer()

    # Load audio file
    with sr.WavFile(audio_path) as source:
        audio = r.record(source)

    # Convert audio to text
    try:
        text = sr.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Speech recognition could not understand audio"
    except sr.RequestError as e:
        return "Could not request results from Google Speech Recognition service; {0}".format(e)

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
