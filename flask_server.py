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

## Transfer File
!pip install paramiko
import paramiko
def transfer_file(remote_path="/home/nao/microphones/recording.wav", local_path="recordings/recording.wav"):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, username='nao', password='nao')

    sftp = ssh.open_sftp()
    sftp.get(remote_path, local_path)

    sftp.close()
    ssh.close()
    print("File transfered")

def receive_file(local_path="recordings/recording.wav", remote_path="/home/nao/microphones/recording.wav"):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, username='nao', password='nao')

    sftp = ssh.open_sftp()
    sftp.put(local_path, remote_path)

    sftp.close()
    ssh.close()

## Audio Recording
def eye_color(status="ListenOn", rgb = None):
    leds = ALProxy("ALLeds", ip, port)

    if rgb is None:
        if status == "ListenOn":
            leds.fadeRGB("AllLeds", "yellow", 1)
        elif status == "SpeechDetected":
            leds.fadeRGB("AllLeds", "green", 8)
        elif status == "EndOfProcess":
            leds.fadeRGB("AllLeds", "white", 1)

    else:
        leds.fadeRGB("Face", rgb, 1)


# Callback function for timer
def timer_callback(timer_cb):
    print("Timer reached")
    timer_cb.set()

# Records Audio when speech is detected
def record_audio(timer=None, path_name="/home/nao/microphones/recording.wav", debug=False):
    path_name = os.path.join(path_name)
    # Create Connection Proxies
    recorder = ALProxy("ALAudioRecorder", ip, port)
    speech_recogniser = ALProxy("ALSpeechRecognition", ip, port)
    sound_detector = ALProxy("ALSoundDetection", ip, port)
    memory = ALProxy("ALMemory", ip, port)

    speech_recogniser.subscribe("speech_recognition")
    speech_recogniser.setLanguage("English")
    vocabulary = ["pepper", "hello"]
    speech_recogniser.setVocabulary(vocabulary, False)

    # Stop recording when speech stops being detected or timer is reached
    timer_cb = threading.Event()
    if timer is not None:
        threading.Timer(timer, timer_callback, timer_cb).start()

    # Start recording
    while True:
        time.sleep(0.5)
        status = memory.getData("ALSpeechRecognition/Status")

        # Print status
        if debug:
            print(status)

        # Start recording when speech is detected
        if status == "SpeechDetected":
            eye_color(status)
            print("Recording is starting...")
            recorder.startMicrophonesRecording(path_name, "wav", 16000, (0,0,1,0))
            break

        # Stop recording when timer is reached
        if timer_cb.is_set():
            break

    if timer_cb.is_set():
        return

    while True:
        time.sleep(0.5)
        status = memory.getData("ALSpeechRecognition/Status")

        # Stop recording when speech stops being detected
        if status == "EndOfProcess":
            print("Recording is stopping...")
            recorder.stopMicrophonesRecording()
            speech_recogniser.unsubscribe("speech_recognition")
            eye_color(status)
            break

        # Stop recording when timer is reached
        if timer_cb.is_set():
            recorder.stopMicrophonesRecording()
            speech_recogniser.unsubscribe("speech_recognition")
            leds = ALProxy("ALLeds", ip, port)
            leds.fadeRGB("AllLeds", "White", 1)
            break


def record_audio_sd(timer=None, path_name="/home/nao/microphones/recording.wav", debug=False):
    path_name = os.path.join(path_name)
    # Create Connection Proxies
    recorder = ALProxy("ALAudioRecorder", ip, port)
    sound_detector = ALProxy("ALSoundDetection", ip, port)
    memory = ALProxy("ALMemory", ip, port)
    
    timer_cb = threading.Event()

    sound_detector.subscribe("sound_detector")
    sound_detector.setParameter("Sensitivity", 0.8)

    # Record audio when sound is detected
    if timer is not None:
        threading.Timer(timer, timer_callback, [timer_cb]).start()

    # Start recording
    while True:
        time.sleep(0.5)
        status = memory.getData("SoundDetected")

        # Print status
        if debug:
            print(status)

        # Start recording when sound is detected
        if status is not None:
            print("Recording is starting...")
            recorder.startMicrophonesRecording(path_name, "wav", 16000, (0,0,1,0))
            eye_color("SpeechDetected")
            break

        # Stop recording when timer is reached
        if timer_cb.is_set():
            break

    if timer_cb.is_set():
        return
    
    sound_detector.setParameter("Sensitivity", 0.7)
    while True:
        time.sleep(3)
        status = memory.getData("SoundDetected")

        if debug:
            print("Status: ", status)

        # Stop recording when sound stops being detected
        if status is None:
            print("Recording is stopping...")
            recorder.stopMicrophonesRecording()
            sound_detector.unsubscribe("sound_detector")
            leds = ALProxy("ALLeds", ip, port)
            leds.fadeRGB("AllLeds", "white", 1)
            break

        # Stop recording when timer is reached
        if timer_cb:
            print("Recording is stopping...")
            recorder.stopMicrophonesRecording()
            sound_detector.unsubscribe("sound_detector")
            leds = ALProxy("ALLeds", ip, port)
            leds.fadeRGB("AllLeds", "white", 1)
            break

## Speech to Text
!pip install speechrecognition==3.8.1
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

@app.route('/say', methods=['POST'])
def say_something():
    data = request.form.to_dict()
    speech_proxy.say(str(data['message']))
    return 'OK'

@app.route('/stopSay', methods=['POST'])
def stop_say():
    speech_proxy.stopAll()
    return 'OK'

@app.route('/listen', methods=['POST'])
def listen():
    record_audio_sd(timer=15, debug=False)
    transfer_file()
    text = convert_wav_to_text("recordings/recording.wav")
    return jsonify({'text': text})

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