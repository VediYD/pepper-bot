from flask import Flask, request, jsonify

from scipy.io import wavfile
import noisereduce as nr
import numpy as np
import speech_recognition as sr
import soundfile as sf

app = Flask(__name__)

@app.route('/noise', methods=['POST'])
def noise_reducer():
    # Get the audio file path
    data = request.json
    path = str(data['audio_loc'])
    sav_loc = str(data['save_loc'])
    prop_decrease = float(data['prop_decrease'])
    vol_increase = float(data['vol_increase'])

    # Load Data
    rate, data = wavfile.read(path)
    
    # Noise Data
    n_rate, n_data = wavfile.read("recordings/noise.wav")

    # Reduce noise
    reduced_noise = nr.reduce_noise(y=data, 
                                    sr=rate, 
                                    y_noise=n_data,
                                    prop_decrease=prop_decrease, 
                                    n_jobs=-1)

    # Increase volume (make up for the volume reduction)
    reduced_noise = reduced_noise * vol_increase

    # Convert to 16-bit data
    reduced_noise = reduced_noise.astype(np.int16)

    # Save the output
    if sav_loc != '':
        wavfile.write(sav_loc, rate, reduced_noise)
    else:
        sav_loc = "recordings/rn_recording.wav"
        wavfile.write(sav_loc, rate, reduced_noise)

    return 'Saved noise reduced audio file to ' + sav_loc

@app.route('/speechtotext', methods=['POST'])
def speech_to_text():
    # Get the audio file path
    data = request.json
    path = str(data['audio_loc'])
    engine = str(data['engine'])

    # Initialize recognizer class (for recognizing the speech)
    r = sr.Recognizer()

    # Convert the audio to speech
    with sr.AudioFile(path) as source:
        # Listen for the data (load audio to memory)
        audio_data = r.record(source)
        # Recognize the text
        text = None
        if engine == 'google':
            text = r.recognize_google(audio_data)
        elif engine == 'sphinx':
            text = r.recognize_sphinx(audio_data)
        elif engine == 'ibm':
            text = r.recognize_ibm(audio_data)

    return text


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8891)
