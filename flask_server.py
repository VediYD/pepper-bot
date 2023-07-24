from flask import Flask, request
from naoqi import ALProxy

app = Flask(__name__)
record_proxy = ALProxy("ALAudioRecorder", "192.168.0.192", 9559)

#from flask import Flask, request
#import qi

#app = Flask(__name__)
#session = None
#audio_recorder = None

# Connect to the robot and get the ALAudioRecorder service
#@app.before_first_request
#def connect_to_robot():
#    global session, audio_recorder
#    session = qi.Session()
#    session.connect("tcp://192.168.0.192:9559")
#    audio_recorder = session.service("ALAudioRecorder")

# Route to start audio recording
@app.route("/record_audio", methods=["POST"])
def record_audio():
    if request.method == "POST":
        action = request.form.get("action")

        if action == "start":
            
            # Set the output file path
            output_file = "recorded_audio.wav"
            
            # Set the audio format
            sample_rate = 16000
            channels = [0, 0, 1, 0]  # Record only from the front microphones

            # Start recording audio
            audio_recorder.startMicrophonesRecording(output_file, "wav", sample_rate, channels)

            return "Recording started"
        elif action == "stop":
            # Stop recording audio
            audio_recorder.stopMicrophonesRecording()

            return "Recording stopped"
        
@app.route('/say', methods=['GET'])
def say_something():
    message = "तुम्ही कसे आहात?"
    data = request.args.to_dict()
    speech_proxy.say(str(data['message']))
    return 'OK'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8891)
    
    
    
speech_proxy = ALProxy("ALTextToSpeech", "192.168.0.192", 9559)
speech_proxy.setLanguage("marathi")  # Update the language code to 'marathi'




    
