from flask import Flask, request, jsonify
from pocketsphinx import LiveSpeech

app = Flask(__name__)

@app.route('/convert_audio', methods=['POST'])
def convert_audio():
    # Check if the 'audio' file is present in the request
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'})

    audio_file = request.files['audio']

    # Save the uploaded file
    audio_path = 'recordings/' + audio_file.filename
    audio_file.save(audio_path)

    # Convert audio to text
    result = convert_wav_to_text(audio_path)

    # Return the converted text
    return jsonify({'text': result})

def convert_wav_to_text(audio_path):
    speech = LiveSpeech(
        verbose=False,
        sampling_rate=16000,
        buffer_size=2048,
        no_search=False,
        full_utt=False,
        lm=False
    )

    result = ''
    for phrase in speech:
        result += str(phrase) + ' '

    return result.strip()

if __name__ == '__main__':
    app.run(debug=True)
