combinedGreetingAndGenericPrompts = [
    "Hi! I'm Pepper. How can I assist you?",
    "Hello there! How may I help?",
    "Hello! I'm Pepper, your friendly robot.",
    "Hi there! How can I assist you?",
    "Greetings! What can I do for you today?",
    "Hey! Nice to see you!",
    "Good day! How may I help you?",
    "Welcome! How can I be of service?",
    "Hello! I'm here to make your day better.",
    "Hey! What brings you here?",
    "Hi! How's your day going so far?",
    "Greetings, my friend!",
    "Hello there! I'm always ready to chat.",
    "Hi! I'm Pepper, your helpful companion.",
    "Hey, it's me again! How can I assist you this time?",
    "Good to see you! How can I brighten your day?"
]

basicGreetings = [
    "Hi! I'm Pepper. Welcome to Deakin Open Day!",
    "Hello, I'm Pepper. It's great to see you at our Open Day.",
    "Hello, my name is Pepper.",
    "Hi there, I'm Pepper!",
    "Hello and welcome to Open Day! You can call me Pepper.",
    "Greetings, my name is Pepper and I'm a friendly robot from Deakin University."
]

basicTopicPrompts = [
    "I'm here to help you find out more about things like our courses and student life. Do you have any questions for me?",
    "I have a lot of information about our degrees and campus activities. What would you like to know more about?",
    "I can tell you all about our amazing programs and facilities. What are you interested in studying?",
    "I would love to help you discover our courses and learning resources. What are your strengths and challenges?",
    "I am here to answer your questions about studying at Deakin! What are you looking for?" 
]

basicCoursePrompt = [
    "I am happy to answer questions about specific courses, is there one in particular you are interested in?",
]

courseInterlude = [
    "To answer questions about specific courses, it will just take me a second to think!"
]

confusionInterlude = [
    "Uh... sorry. I think I got confused. What were we talking about?"
]

confusionRepeat = [
    "Sorry, I got confused. Could you frame your question differently?", 
    "Sorry, I got confused. Can we start again?"
]

combinedTopicPrompts = [
    "Deakin offers a wide range of courses across different disciplines and levels. What are you interested in studying?",
    "Deakin is a leading university in research and innovation, with many opportunities for students to get involved. Are you curious about our research areas and projects?",
    "Deakin has a vibrant and diverse student community, with many clubs, societies and events to enjoy. Would you like to hear about activities?",
    "Deakin has four campuses across Victoria, each with its own unique features and facilities. Which campus are you planning to visit or study at?",
    "Deakin has a flexible and supportive learning environment, with many options for online and blended delivery. How do you prefer to learn and study?"
]

tieredConfusionPrompts = [
    "I didn't quite catch that. Could you please repeat it?", 
    "Uh... sorry. Please try again.", 
    "I'm so sorry. I'm having trouble hearing you. Could you try moving closer and speaking louder, into my microphones?", 
    "I still could not hear you. I'm so sorry, I might be runnning too hot. Please excuse me while I take a moment to reset. Thank-you for interacting with me!"
]

goodbyePrompts = [
    # "Uh... sorry. I think I got confused. What were we talking about?"
    "Thanks for stopping by! It was lovely to talk to you. ", 
    "I appreciate you coming by to say hello! Have a good rest of your day. ",
    "I hope was able to help! Thanks for the chat.",
    "Thanks for the conversation, it was lovely having you here!"
]

verificationPrompts = {
    "Cour":"Just to check, was your question about Courses?",
    "Cacc":"Just confirming, did you ask about accommodation?",
    "Club":"Oh, are you referring to the Deakin clubs and activities? Just confirming to make sure that I'm providing you with the correct information!",
    "Cgen":"",
    "Camp":"Could you please confirm if your question was about the Deakin Campuses?",    
    "Cspe":""            
}

topicBlurb = {
    "Cour":"Just to check, was your question about Courses?",
    "Cacc":"Exploring accommodations? Great choice! Simply glance at the QR code on my screen for all the essential info. Whenever you're ready, go ahead and give it a scan!",
    "Club":"At Deakin, there are lots of fun activities to get involved in - too many for me to list! This Q-R code will take you right to the details.",
    "Cgen":"",
    "Camp":"Sure thing! Scan the QR code on my screen for a sneak peek into our campuses. Enjoy all the exciting details at your convenience!", 
    "Cspe":""              
}

noExamples = [
    "negative", "nope", "not at all", 
    "certainly not", "absolutely not", "not really", 
    "by no means", "deny", "decline", 
    "refuse", "reject", "disagree", 
    "nix", "no way", "never", 
    "nada", "i don't think so", "nah", 
    "i disagree", "i'm afraid not"
]

yesExamples = [
    "affirmative", "absolutely", "indeed", 
    "certainly", "absolutely right", "correct", 
    "that's true", "you bet", "precisely", 
    "of course", "without a doubt", "sure thing", 
    "definitely", "by all means", "yup",
    "that's correct", "agreed", "positively", 
    "true", "absolutely", "yes"
]

nextTopicPrompts = [
    "Is there anything else I could help you with today?", 
    "Is there anything else you'd like to know?", 
    "Do you have any other questions?",
    "Is there something else on your mind?", 
    "Are there additional topics you'd like to explore?"
]

accommodationKeywordExamples = [
    "accommodation", "lodging","live","rent","room","res","resident","residential"
]

activitiesKeywordExamples = [
    "activity", "activities","club","clubs","organization","extracurricular","society","union"
]

coursesKeywordExamples = [
    "course", "bachelor","master","masters","certificate","diploma","horse","hourses", "courses", "degree"
]