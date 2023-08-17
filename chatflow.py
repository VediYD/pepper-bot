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
    


































    # if pred_class=="Campus":
    #     speak("Gotcha! Deakin campuses, right? Just checking so I can give you the right info!")
    #     # showWhichPage("Confirm")
        
    #     txt = listen()
            
    #     found_yes = any(synonym in txt.lower() for synonym in yes)

    #     if found_yes:
    #         speak("Absolutely! If you're interested in learning more about our campuses, I've got you covered. Just take a look at the QR code displayed on my screen, and it will provide you with all the exciting details about our wonderful campuses. Feel free to scan it whenever you're ready!")
    #         showWhichPage("Camp")
    #         time.sleep(0.5)
            
            
    #     #found_no = any(synonym in txt.lower() for synonym in no)
    #     #elif found_no:
    #     #    speak("No worries, Let's start again")
    #     #    break
    #     #    # Idle behaviors to keep peppers temperature low
    #     #    idle.start_idle_behavior()
        
    #     else:
    #         speak("No worries, Let's start again")
    #         break
    #         # Idle behaviors to keep peppers temperature low
    #         idle.start_idle_behavior()
            
    # ## TODO: Elif for Courses

        
    # elif pred_class=="Accomodation":
    #     speak("Got it! Looking into accommodation at Deakin, correct? Just double-checking to provide the best details!")
    #     #showWhichPage("Confirm")
        
    #     txt = listen()
        
    #     found_yes = any(synonym in txt.lower() for synonym in yes)

    #     if found_yes:
    #         speak("")
    #         showWhichPage("Cacc")
    #         time.sleep(0.5)
            
    #     #found_no = any(synonym in txt.lower() for synonym in no)
    #     #elif found_no:
    #     #    speak("No worries, Let's start again")
    #     #    break
    #     #    # Idle behaviors to keep peppers temperature low
    #     #    idle.start_idle_behavior()
        
    #     else:
    #         speak("No worries, Let's start again")
    #         break
    #         # Idle behaviors to keep peppers temperature low
    #         idle.start_idle_behavior()
        
        
    # elif pred_class=="Activities":
    #     speak("Exploring clubs and activities at Deakin, perhaps? Just confirming to provide you with the right information!")
    #     #showWhichPage("Confirm")
        
    #     txt = listen()
        
    #     found_yes = any(synonym in txt.lower() for synonym in yes)

    #     if found_yes:
    #         speak("Ready to uncover the exciting realm of Deakin's clubs and activities? Swing your attention to the QR code dancing on my screen. It's your all-access pass to the buzz! Give it a scan whenever you're up for some fun exploration!")
    #         showWhichPage("Club")
    #         time.sleep(0.5)
            
    #     #found_no = any(synonym in txt.lower() for synonym in no) 
    #     #elif found_no:
    #     #    speak("No worries, Let's start again")
    #     #    break
    #     #    # Idle behaviors to keep peppers temperature low
    #     #    idle.start_idle_behavior()
        
    #     else:
    #         speak("No worries, Let's start again")
    #         break
    #         # Idle behaviors to keep peppers temperature low
    #         idle.start_idle_behavior()
    
        
    # elif pred_class=="General":
    #     "Yash's General Code"
        
    # else:
    #     speak("Thinking about courses at Deakin, am I right?")
    #     "Yash's Course Code"