from pandas import DataFrame


temp = {
    'input': [
        "Wow, you're a robot? That's so cool!",
        "Hi Pepper, nice to meet you. You're very cute.",
        "Hello Pepper, I'm looking for some information about Deakin courses. Can you help me with that?",
        'Hi there, Pepper! You seem like a fun robot. Do you have any jokes to tell?',
        "Hello and welcome to you too, Pepper. I'm curious about your personality. What do you like to do?",
        "G'day, Pepper. You're a ripper of a robot. How's it going?",
        "Hi Pepper, you're amazing. I love robots. Can I hug you?",
        'Hello Pepper, nice to see you. You look very smart. What can you do?',
        'Hi there, Pepper. I need some help finding the bathroom. Can you show me the way?',
        "Hello Pepper, you're very helpful. I want to know more about Deakin scholarships. Can you tell me about them?",
        "Hi Pepper, how are you? I'm just browsing around. Do you have any recommendations?",
        'Hello Pepper, my name is John and I am a human visitor at your mercy.',
        "Hello Pepper, thank you for your service. You're doing a great job. Can I give you some feedback?",
        "Hello Pepper, that's a nice name. How did you get it? Can I choose a different name for you?",
        "Hi Pepper, you're so friendly. Do you have any friends? Can I be your friend?",
        "Hi there, Pepper. You're a great companion. Do you have any hobbies? Can I join you?",
        "Hi Pepper, you're awesome. Do you have any feelings? Can I make you happy?",
        "Hello and thank you! I'll call you Pepper. You're a robot with a charm!",
        "Hello and greetings! I won't call you Pepper. You're a robot with a flaw!",
        "Hello and wow! I can call you Pepper? You're a robot with a surprise!"], 
    'label': [
        'C',
        'C',
        'DQ',
        'FQ',
        'FQ',
        'FQ',
        'RQ',
        'FQ',
        'RQ',
        'DQ',
        'RQ',
        'C',
        'RQ',
        'FQ',
        'FQ',
        'FQ',
        'FQ',
        'C',
        'C',
        'C'
    ]
}

DataFrame(temp).to_csv("conversation_types.csv", index=False)