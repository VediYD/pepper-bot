from interactiveControls import showWhichPage
from humanInteractions import speak, listen, queryCourseCode, querySpecificCourse
import time


## --> Please ask Haddie to fix your show which page function <--
# 1. You've not imported it so it won't work
# 2. This file is in the incorrect directory, so ask her where to put it

global repeat

# Yes and No Synonyms
yes = [
        "affirmative", "absolutely", "indeed", 
        "certainly", "absolutely right", "correct", 
        "that's true", "you bet", "precisely", 
        "of course", "without a doubt", "sure thing", 
        "definitely", "by all means", "yup",
        "that's correct", "agreed", "positively", 
        "true", "absolutely", "yes"
]

no = [
    "negative", "nope", "not at all", 
    "certainly not", "absolutely not", "not really", 
    "by no means", "deny", "decline", 
    "refuse", "reject", "disagree", 
    "nix", "no way", "never", 
    "nada", "i don't think so", "nah", 
    "i disagree", "i'm afraid not"
]

# Output on the bases of the class
def campusOutput():
    showWhichPage("Camp")
    speak('''
        Sure thing! Scan the QR code on my screen for a sneak peek into our campuses. 
        Enjoy all the exciting details at your convenience!
    ''') 

def accomodationOutput():
    showWhichPage("Cacc")
    speak('''
        Exploring accommodations? Great choice! 
        Simply glance at the QR code on my screen for all the essential info. 
        Whenever you're ready, go ahead and give it a scan!
    ''')

def activitiesOutput():
    showWhichPage("Club")
    speak('''
        Write up by Sam
    ''')

def generalOutput(query):
    showWhichPage('prompt')
    # Sends to GPT for response
    postCasualQuery(query)

def coursesOutput(query, responsesPipeline, eyes):
    repeat = queryCourseCode(query, responsesPipeline, eyes)
    if not repeat:
        # Pause for users to read the tablet
        time.sleep(2)

def specificCourseOutput(query, responsesPipeline, eyes, rcount):
    repeat = querySpecificCourse(query, responsesPipeline, eyes, rcount)
    if not repeat:
        # Pause for users to read the tablet
        time.sleep(5)
    return repeat

# Confirm the class and threshold
def convFlow(query, pred_class, threshold, responsesPipeline, eyes, rcount):
    repeat = False
    # If classfier identifies class as Campus
    if pred_class=="Campus":
        # If confidence is above threshold
        if threshold:
            # Shows the campus page and speaks about the following
            campusOutput()           
            
            # Optionally add time.sleep if required
        
        # If confidence is below threshold
        else:
            # Asks the user to confirm if they are referring to the Deakin campuses
            speak('''
                Oh, are you referring to the Deakin campuses? 
                Just confirming to make sure I'm providing you with the correct information!
            ''')

            # Convert the text to speech
            text = listen()
            
            # Check if any of the synonyms of yes are in the text
            found_yes = any(synonym in text.lower() for synonym in yes)
            
            # If yes, show the campus page and speak about the following
            if found_yes:
                campusOutput()

            
            else:
                speak("Sorry, I got confused, could you frame your question differently?")
            

    elif pred_class=="Accomodation":
        if threshold:
            accomodationOutput()
        
        else:
            # Asks the user to confirm if they are referring to the Deakin campuses
            speak('''
                Oh, are you referring to the Deakin accommodations?
                Just confirming to make sure that I'm providing you with the correct information!
            ''')

            # Convert the text to speech
            text = listen()

            # Check if any of the synonyms of yes are in the text
            found_yes = any(synonym in text.lower() for synonym in yes)

            # If yes, show the campus page and speak about the following
            if found_yes:
                accomodationOutput()

            else:
                speak("Sorry, I got confused, could you frame your question differently?")

    elif pred_class=="Activities":
        if threshold:
            activitiesOutput()
        
        else:
            # Asks the user to confirm if they are referring to the Deakin campuses
            speak('''
                Oh, are you referring to the Deakin clubs and activities?
                Just confirming to make sure that I'm providing you with the correct information!
            ''')

            # Convert the text to speech
            text = listen()

            # Check if any of the synonyms of yes are in the text
            found_yes = any(synonym in text.lower() for synonym in yes)

            # If yes, show the campus page and speak about the following
            if found_yes:
                activitiesOutput()

            else:
                speak("Sorry, I got confused, could you frame your question differently?")

    elif pred_class=="General":
        generalOutput(query)

    elif pred_class=="Courses":
        coursesOutput(query, responsesPipeline, eyes, rcount)

    else:
        repeat = specificCourseOutput(query, responsesPipeline, eyes, rcount)

    return repeat

