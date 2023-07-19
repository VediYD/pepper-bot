import noisereduce as nr
import numpy as np
import soundfile as sf
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/noise', methods=['POST'])
def noise_reducer():
    data = request.json
    print(data)
    # Load data
    prop_decrease = float(data['prop_decrease'])

    # Assuming audio_file contains the path to the WAV file
    # Read the WAV file and get audio data and sample rate
    audio_data, sample_rate = sf.read("recordings/recording.wav")

    # Apply noise reduction
    reduced_noise = nr.reduce_noise(y=audio_data, sr=sample_rate, prop_decrease=prop_decrease)

    # Now you can pass the 'reduced_noise' to your speech-to-text module
    sf.write("recordings/rn_recording.wav", reduced_noise, sample_rate)

    return ''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8891)