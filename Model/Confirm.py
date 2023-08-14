



## --> Please ask Haddie to fix your show which page function <--
# 1. You've not imported it so it won't work
# 2. This file is in the incorrect directory, so ask her where to put it

def confirm(pred_class):
    import time
    yes = ["affirmative","absolutely","indeed","certainly","absolutely right","correct","that's true","you bet","precisely","of course","Without a doubt","sure thing","definitely","by all means", "yup","that's correct","agreed","positively", "true","absolutely", "yes"]
    no = ["negative", "nope", "not at all", "certainly not", "absolutely not", "not really", "by no means", "deny", "decline", "refuse", "reject", "disagree", "nix", "no way", "never", "nada", "i don't think so", "nah", "i disagree", "i'm afraid not"]

    if pred_class=="Campus":
        speak("Gotcha! Deakin campuses, right? Just checking so I can give you the right info!")
        # showWhichPage("Confirm")
        
        txt = listen()
            
        found_yes = any(synonym in txt.lower() for synonym in yes)

        if found_yes:
            speak("Absolutely! If you're interested in learning more about our campuses, I've got you covered. Just take a look at the QR code displayed on my screen, and it will provide you with all the exciting details about our wonderful campuses. Feel free to scan it whenever you're ready!")
            showWhichPage("Camp")
            time.sleep(0.5)
            
            
        #found_no = any(synonym in txt.lower() for synonym in no)
        #elif found_no:
        #    speak("No worries, Let's start again")
        #    break
        #    # Idle behaviors to keep peppers temperature low
        #    idle.start_idle_behavior()
        
        else:
            speak("No worries, Let's start again")
            break
            # Idle behaviors to keep peppers temperature low
            idle.start_idle_behavior()
            
    ## TODO: Elif for Courses

        
    elif pred_class=="Accomodation":
        speak("Got it! Looking into accommodation at Deakin, correct? Just double-checking to provide the best details!")
        #showWhichPage("Confirm")
        
        txt = listen()
        
        found_yes = any(synonym in txt.lower() for synonym in yes)

        if found_yes:
            speak("Exploring accommodations? Great choice! Simply glance at the QR code on my screen for all the essential info. Whenever you're ready, go ahead and give it a scan!")
            showWhichPage("Cacc")
            time.sleep(0.5)
            
        #found_no = any(synonym in txt.lower() for synonym in no)
        #elif found_no:
        #    speak("No worries, Let's start again")
        #    break
        #    # Idle behaviors to keep peppers temperature low
        #    idle.start_idle_behavior()
        
        else:
            speak("No worries, Let's start again")
            break
            # Idle behaviors to keep peppers temperature low
            idle.start_idle_behavior()
        
        
    elif pred_class=="Activities":
        speak("Exploring clubs and activities at Deakin, perhaps? Just confirming to provide you with the right information!")
        #showWhichPage("Confirm")
        
        txt = listen()
        
        found_yes = any(synonym in txt.lower() for synonym in yes)

        if found_yes:
            speak("Ready to uncover the exciting realm of Deakin's clubs and activities? Swing your attention to the QR code dancing on my screen. It's your all-access pass to the buzz! Give it a scan whenever you're up for some fun exploration!")
            showWhichPage("Club")
            time.sleep(0.5)
            
        #found_no = any(synonym in txt.lower() for synonym in no) 
        #elif found_no:
        #    speak("No worries, Let's start again")
        #    break
        #    # Idle behaviors to keep peppers temperature low
        #    idle.start_idle_behavior()
        
        else:
            speak("No worries, Let's start again")
            break
            # Idle behaviors to keep peppers temperature low
            idle.start_idle_behavior()
    
        
    elif pred_class=="General":
        "Yash's General Code"
        
    else:
        speak("Thinking about courses at Deakin, am I right?")
        "Yash's Course Code"