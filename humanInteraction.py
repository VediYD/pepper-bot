### Custom File Handing Imports ###
from fileTransfer import *

### Custom Idle Behaviour Imports ###
from idle import *

### Custom Page Display Imports ###
from displayGeneration import *

### Custom Interaction, Behaviour and Display Imports ###
from interactiveControls import *

### Custom Hard-Coded Prompt Imports ###
from prompts import *

### Main Interaction Imports ###
from humanInteraction import *

import prompts
import constants
import interactiveControls as ic

################################################################################
##### Function Handles
##########

def detect():
    seePersonAndGreet()
    print("Detect complete")

def listen():
    record_audio_sd(timer=15, debug=False)
    sendFromPepper()
    # reduce_noise()
    text = convert_wav_to_text('recordings/recording.wav')
    print('Listen complete, This is what I heard: ', text)
    return text

def speak(text):
    tts = ALProxy("ALTextToSpeech", constants.PEPPER_HOST, constants.PEPPER_PORT)
    tts.say(text)

def shush():
    tts = ALProxy("ALTextToSpeech", constants.PEPPER_HOST, constants.PEPPER_PORT)
    tts.stopAll()

def think(query, responsesPipeline, eyes):
    eyes.start_thinking()
    # show_on_tablet('Demo/pageTemplates/dashLoader.html')
    ic.showWhichPage("loading")
    postQuery(query, responsesPipeline) #postQuery(_question, sentences):
    eyes.stop_thinking()
    ic.resetEyesAndTablet()

################################################################################
##### Detect Person
##########

def seePersonAndGreet():
    # Imports
    memory = ALProxy("ALMemory", constants.PEPPER_HOST, constants.PEPPER_PORT)
    tracker = ALProxy("ALTracker", constants.PEPPER_HOST, constants.PEPPER_PORT)
    face_detection = ALProxy("ALFaceDetection", constants.PEPPER_HOST, constants.PEPPER_PORT)

    face_detection.subscribe("FaceDetection")
    tracker.registerTarget("Face", 0.1)
    tracker.setMode("Head")
    tracker.track("Face")
    tracker.setMaximumDistanceDetection(0.1)
    ic.showWhichPage('prompt')
    is_detected = False
    greeting = ""
    while not is_detected:
        faces = memory.getData("FaceDetected")
        if faces and isinstance(faces, list) and len(faces) > 0:
            face_info = faces[0]
            face_id = face_info[0]
            pos = tracker.getTargetPosition(0)
            now = time.time()
            print(pos[0])
            while face_id >= 0 or pos[0] <= 0.85:
                if time.time() - now > 3:
                    is_detected = True
                    # Say a random greeting from the list
                    greeting = getGreeting() #= random.choice(greetings)
                    break
        speak(greeting)



def getGreeting():
    """Get greeting from other file as basicGreeting ("Hello, I'm Pepper") + basicTopicPrompts ("Ask me about...")"""
    greeting = random.choice(prompts.basicGreetings) + random.choice(prompts.basicTopicPrompts)
    return greeting



# ################################################################################
# ##### Pepper Speaks
# ##########

# def speak(text):
#     tts = ALProxy("ALTextToSpeech", constants.PEPPER_HOST, constants.PEPPER_PORT)
#     tts.say(text)



################################################################################
##### Listen for Query
##########

def timer_callback(timer_cb):
    """To cut off audio collection after given timelimit (hardcoded in record_audio_sd)"""
    timer_cb.set()
    
def record_audio_sd(timer=None, path_name="/home/nao/microphones/recording.wav", debug=False):
    """complete audio subscription, detection, recording start and stop"""
    path_name = os.path.join(path_name)

    # Create Connection Proxies
    recorder = ALProxy("ALAudioRecorder", constants.PEPPER_HOST, constants.PEPPER_PORT)
    sound_detector = ALProxy("ALSoundDetection", constants.PEPPER_HOST, constants.PEPPER_PORT)
    memory = ALProxy("ALMemory", constants.PEPPER_HOST, constants.PEPPER_PORT)
    
    sound_detector.subscribe("sound_detector")
    sound_detector.setParameter("Sensitivity", 0.9)

    # Callback function for timer
    timer_cb = threading.Event()

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
            set_leds('cyan')
            break

        # Stop recording when timer is reached
        if timer_cb.is_set():
            break

    if timer_cb.is_set():
        recorder.stopMicrophonesRecording()
        sound_detector.unsubscribe("sound_detector")
        return
    
    sound_detector.setParameter("Sensitivity", 0.5)
    while True:
        time.sleep(0.5)
        status = memory.getData("SoundDetected")

        if debug:
            print("Status: ", status)

        # Stop recording when sound stops being detected
        if status is None:
            print("Recording is stopping...")
            recorder.stopMicrophonesRecording()
            sound_detector.unsubscribe("sound_detector")
            break

        # Stop recording when timer is reached
        if timer_cb.is_set():
            print('Timer is reached')
            print("Recording is stopping...")
            recorder.stopMicrophonesRecording()
            sound_detector.unsubscribe("sound_detector")
            break



################################################################################
##### Convert audio to text
##########

### WE WILL USE SOMETHING ELSE WHICH WORKS BETTER
def reduce_noise(server, path = '', amount = 0.9):
    """Depreciated"""
    requests.post(server + '/noise', json={'prop_decrease': amount, 'path': path})

### WE WILL USE SOMETHING ELSE WHICH WORKS BETTER
def convert_wav_to_text(audio_path):
    """Depreciated"""
    r = sr.Recognizer()

    with sr.AudioFile(audio_path) as source:
        r.adjust_for_ambient_noise(source)
        audio_data = r.record(source)

    try:
        text = r.recognize_sphinx(audio_data)
        return text
    except sr.UnknownValueError:
        return "Speech recognition could not understand audio"
    except sr.RequestError as e:
        return "Could not request results from Google Speech Recognition service: " + str(e)
    except Exception as e:
        return "An error occurred during speech recognition: " + str(e)



################################################################################
##### GPT text reciever
##########

# global c_code

def say_sentences_thread(sentences):
    # df = pd.read_csv('pages/textbyID.csv')
    # courseID = df['ID'].tolist()
    # check_ID = True
    while True:
        if len(sentences) != 0:

            # if check_ID:
            #     check_ID = False
            #     for word in courseID:
            #         if word in sentences[0]:
            #             c_code = str(sentences[0].split(',')[0])
            #             print('Course Code: ' + c_code)

            if sentences[0] == "quit":
                break  
             
            speak(sentences[0])
            sentences.pop(0)

        else:
            time.sleep(1)
            continue
    print('Stopped')

def receive_responses(response, sentences):
    say_thread = threading.Thread(target=say_sentences_thread, args=(sentences,))
    say_thread.start()
    for line in response.iter_content(chunk_size=None):
        x = str(line.decode('utf-8'))
        print(x)
        sentences.append(x)
    say_thread.join()

def postQuery(_question, sentences):
    url = 'http://10.104.22.24:8891/courseInfo'
    # url = "http://{}:{}/courseInfo".format(GPT_HOST, GPT_PORT)
    data = {"question": _question}
    r = requests.post(url, json=data, stream=True)
    receive_responses(r, sentences)

def stopListening():
    recorder = ALProxy("ALAudioRecorder", constants.PEPPER_HOST, constants.PEPPER_PORT)
    recorder.stopMicrophonesRecording()