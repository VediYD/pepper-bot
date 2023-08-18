# from urllib import response
from naoqi import ALProxy

from prompts             import basicGreetings, basicTopicPrompts
from constants           import PEPPER_HOST, PEPPER_PORT
from requests            import post
from time                import time, sleep
from random              import choice
from threading           import Timer, Event, Thread
from os.path             import join as path_join
from fileTransfer        import sendFromPepper
from interactiveControls import showWhichPage, resetEyesAndTablet, set_leds
from interactiveControls import showPage
from displayGeneration   import seekCourseName, generateListeningPage
from displayGeneration   import generateBasicListViewPage, generateBasicQRPage

from scipy.io import wavfile
import speech_recognition as sr
import numpy as np

################################################################################
##### Function Handles
##########

global link
link = 'http://10.104.22.24:8891'

def detect(_idle):
    seePersonAndGreet(_idle)
    print("Detect complete")

    
def listen():
    showWhichPage("listening")
    record_audio_sd(timer=8, debug=False)
    sendFromPepper()
    reduce_noise(link)
    text = convert_wav_to_text('recordings/recording.wav')
    
    print('Listen complete, This is what I heard: ', text)
    return text


def speak(text):
    tts = ALProxy("ALAnimatedSpeech", PEPPER_HOST, PEPPER_PORT)
    tts.say('^mode(contextual) ' + text + ' ^mode(disabled)')

    
def shush():
    tts = ALProxy("ALTextToSpeech", PEPPER_HOST, PEPPER_PORT)
    tts.stopAll()
    

def queryCourseCodes(query, responsesPipeline, eyes):
    eyes.setEyes("thinking")
    showWhichPage("loading")
    # queryCourseCodes returns "repeat" = true if the query search is not successful
    repeat = postQueryCourseCodes(query, responsesPipeline)
    eyes.setEyes("neutral")
    return repeat


def querySpecificCourse(query, responsesPipeline, eyes, rcnt):
    eyes.setEyes("thinking")
    # queryCourseCodes returns "repeat" = true if the query search is not successful
    repeat = postQuerySpecificCourse(query, responsesPipeline, rcnt)
    eyes.setEyes("neutral")
    return repeat


################################################################################
##### Detect Person
##########

def faceTracker():
    tracker = ALProxy("ALTracker", PEPPER_HOST, PEPPER_PORT)
    tracker.registerTarget("Face", 0.1)
    tracker.setMode("Head")
    tracker.track("Face")
    tracker.setMaximumDistanceDetection(0.1)


def seePersonAndGreet(_idle):
    # Imports
    memory = ALProxy("ALMemory", PEPPER_HOST, PEPPER_PORT)
    tracker = ALProxy("ALTracker", PEPPER_HOST, PEPPER_PORT)
    face_detection = ALProxy("ALFaceDetection", PEPPER_HOST, PEPPER_PORT)

    face_detection.subscribe("FaceDetection")
    tracker.registerTarget("Face", 0.1)
    tracker.setMode("Head")
    tracker.track("Face")
    tracker.setMaximumDistanceDetection(0.1)
    showWhichPage('prompt')
    is_detected = False
    greeting = ""
    while not is_detected:
        faces = memory.getData("FaceDetected")
        if faces and isinstance(faces, list) and len(faces) > 0:
            face_info = faces[0]
            face_id = face_info[0]
            pos = tracker.getTargetPosition(0)
            now = time()
            print(pos[0])
            while face_id >= 0 or pos[0] <= 0.85:
                if time() - now > 3:
                    is_detected = True
                    _idle.stop()
                    # Say a random greeting from the list
                    greeting = getGreeting() #= choice(greetings)
                    break
        speak(greeting)


def getGreeting():
    """Get greeting from other file as basicGreeting ("Hello, I'm Pepper") + basicTopicPrompts ("Ask me about...")"""
    greeting = choice(basicGreetings) + choice(basicTopicPrompts)
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
    path_name = path_join(path_name)

    # Create Connection Proxies
    recorder = ALProxy("ALAudioRecorder", PEPPER_HOST, PEPPER_PORT)
    sound_detector = ALProxy("ALSoundDetection", PEPPER_HOST, PEPPER_PORT)
    memory = ALProxy("ALMemory", PEPPER_HOST, PEPPER_PORT)
    
    sound_detector.subscribe("sound_detector")
    sound_detector.setParameter("Sensitivity", 0.9)

    # Callback function for timer
    timer_cb = Event()

    # Record audio when sound is detected
    if timer is not None:
        Timer(timer, timer_callback, [timer_cb]).start()

    # Start recording
    while True:
        status = memory.getData("SoundDetected")

        # Print status
        if debug:
            print(status)

        # Start recording when sound is detected
        if status is not None:
            print("Recording is starting...")
            generateListeningPage()                          
            showPage()
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

            
def stopListening():
    recorder = ALProxy("ALAudioRecorder", PEPPER_HOST, PEPPER_PORT)
    recorder.stopMicrophonesRecording()


################################################################################
##### Convert audio to text
##########

# Reduces the fan noise in recordings
def reduce_noise(server, audio_path = 'recordings/recording.wav', save_path = 'recordings/rn_recording.wav', amount = 0.4, vol_increase = 5):
    # Read the audio file
    rate, data = wavfile.read(audio_path)
    
    # Send to flask
    reduced_noise = np.array(post(server + '/denoise', json={
        'rate': rate, 
        'data': data.tolist(),
        'prop_decrease': amount, 
        'vol_increase' : vol_increase
    }).json()['rn'], dtype=np.int16)

    print(reduced_noise)
    print(type(reduced_noise))

    np.array(reduced_noise)

    wavfile.write(save_path, rate, reduced_noise)

    print('Saved noise reduced audio file to ' + save_path)

def convert_wav_to_text(audio_path, engine='google'):
    try:
        # Initialize recognizer class (for recognizing the speech)
        r = sr.Recognizer()

        # Convert the audio to speech
        with sr.AudioFile(audio_path) as source:
            # Listen for the data (load audio to memory)
            audio_data = r.record(source)
            # Recognize the text
            text = None
            if engine == 'google':
                text = r.recognize_google(audio_data)
            elif engine == 'sphinx':
                text = r.recognize_sphinx(audio_data)

        return text

    except Exception as e:
        print(e)
        return '%low_volume_error%'
    
def check_lowvol(_ques):
    if _ques=='%low_volume_error%':
        print('Low volume error reached')
        speak("Sorry that was difficult for me to understand. Can you please speak a bit louder.")
        return True
    else:
        return False


################################################################################
##### GPT text reciever
##########

def classifyQuery(query, threshold=0.8):
    url = link + '/classifyResponse'
    data = {"sentence": query, "threshold": threshold}
    response = post(url, json=data)
    label = response.json()['label']
    abv_thresh = response.json()['abv_thresh']
    return label, abv_thresh


def postQueryCourseCodes(_question, sentences):
    _lowvol = check_lowvol(_question)
    if _lowvol:
        # if low volume repeat the last prompt
        return True
    url = link + '/getCourses'
    data = {"question": _question}
    response = post(url, json=data, stream=True)
    course_codes = response.json()['course_codes']
    
    if len(course_codes):
        course_names = [seekCourseName(str(i)) for i in course_codes]
        generateBasicListViewPage([str(i) for i in course_codes[:5]])                    
        showPage()
        if len(course_names) == 0:
            ### redundant? but just in case
            speak("Sorry, I couldn't find any courses like that.")
            speak("Did you have a specific course in mind?")
        elif len(course_names) == 1:
            # if course_names len = 1, use different grammar
            speak("I have found one course for you.")
            speak("It is the " + course_names[0])
            speak("Would you like to know more about this course?")
        else:
            # if course_names len > 1, use plural language
            speak('I have found {} courses for you.'.format(len(course_codes)))
            speak('Here are a few that you might find interesting.')
            speak(str(', '.join(course_names[:3])))
            speak('Do you wanna know more about a specific course?')
        return False
    else:
        speak('I am unable to find any relevant courses for you. Can you please repeat your query?')
        return True
    
    
def postQuerySpecificCourse(_question, sentences, rcnt):
    _lowvol = check_lowvol(_question)
    if _lowvol:
        # if low volume repeat the last prompt
        return True
    url = link + '/courseInfo'
    data = {"question": _question}
    response = post(url, json=data, stream=True)
    course_summary = str(response.json()['course_summary'])
    course_code = str(response.json()['course_code'])
    print(course_summary, course_code)
    
    if len(course_summary):   # if at least one course summary is returned
        generateBasicQRPage(course_code) # show the QR page for the first
        showPage()
        speak(course_summary) # say the summary for the first (these should be the same course, but need to confirm how the query function works!)
        return False
    else:
        if rcnt < 4:
            speak('Sorry could you please repeat that?')
            return True
        else:
#             resetEyesAndTablet()
            speak('Sorry I am unable to understand. My processors might be running hot. I need some rest. But thank you for interacting with me.')
            return False
    
def postCasualQuery(_question, sentences):    
    # define the link to the casual query to gpt
    url = link + '/casualQuery'
    
    # construct the data structure to send post request
    data = {'question': _question}
    
    # set stream=True to allow streaming response back - done at gpt's side
    response = post(url, json=data, stream=True)
    
    speak(response.json().encode('utf-8'))


def postQueryToGPTStreamer(_question, sentences):
    url = link + '/getCourses'
    data = {"question": _question}
    response = post(url, json=data, stream=True)
    
    # Sentences Thread
    say_thread = Thread(target=say_sentences_thread, args=(sentences,))
    say_thread.start()
    for line in response.iter_content(chunk_size=None):
        x = str(line.decode('utf-8'))
        print(x)
        sentences.append(x)
    say_thread.join()

    
def say_sentences_thread(sentences):
    print(sentences)
    counter = 0
    
    # initially nothing is spoken
    spoken = False
    
    # forever
    while True:
        
        # if nothing to say
        if len(sentences) != 0:
            
            # thread exit condition
            if sentences[0] == "quit":
                break  
            
            # say the sentence
            speak(sentences[0])
            
            # remove it from the sentence list
            sentences.pop(0)
            
            # record the time at which last sentence was said
            counter = time()
            
            # something has been said now
            spoken = True
        else:
            # wait only for 10 seconds after last spoken
            if ((time() - counter) > 10) & spoken:
                
                # after 10 seconds no point in waiting longer
                break
            else:
                # if no sentences to say, nothing has been said
                sleep(1)  # do nothing
            continue
