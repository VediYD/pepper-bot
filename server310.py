from flask import Flask, request, jsonify

import noisereduce as nr
import speech_recognition as sr
import numpy as np
import soundfile as sf

app = Flask(__name__)

@app.route('/noise', methods=['POST'])
def noise_reducer():
    try:
        data = request.json
        print(data)
        # Load data
        prop_decrease = float(data['prop_decrease'])
        path = str(data['path'])

        if path != '':
            audio_data, sample_rate = sf.read(path)
        else:
            audio_data, sample_rate = sf.read("recordings/recording.wav")

        # Assuming audio_file contains the path to the WAV file
        # Read the WAV file and get audio data and sample rate

        # Apply noise reduction
        reduced_noise = nr.reduce_noise(y=audio_data, sr=sample_rate, prop_decrease=prop_decrease)

        # Now you can pass the 'reduced_noise' to your speech-to-text module
        sf.write("recordings/rn_recording.wav", reduced_noise, sample_rate)

        return 'Reduced'
    except:
        return 'Error'

@app.route('/stt', methods=['POST'])
def speech_to_text():
    data = request.json
    audio_path = str(data['path'])

    r = sr.Recognizer()
    audio = sr.AudioFile(audio_path)
    
    with audio as source:
        audio_file = r.record(source)
        result = r.recognize_sphinx(audio_file)

    print(result)
    return result

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8891, debug=True)