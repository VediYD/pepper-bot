from flask import Flask, request, jsonify, Response
from numpy.random import choice, randint
from time import sleep

import asyncio
from aiohttp import web


print('imports complete')

sample_responses = [
    "Our academic course catalog offers a wide range of courses that cover various disciplines, including science, technology, engineering, arts, and mathematics. From advanced quantum physics to creative writing workshops, we strive to provide diverse learning opportunities for students.",
    "This is a short response.",
    "Exploring the world of academia, you'll find our courses designed to ignite intellectual curiosity. Dive deep into the intricacies of ancient civilizations or navigate the complexities of modern data science. Each course is a journey, an exploration of knowledge waiting to be uncovered.",
    "The weather has been great recently.",
    "In the realm of academic excellence, our courses stand as pillars of wisdom. Whether you're drawn to unraveling the mysteries of the human mind through psychology courses or delving into the frontiers of artificial intelligence, our curriculum caters to your thirst for learning.",
    "Welcome to our academic universe where courses serve as constellations of knowledge. Embark on a voyage through history, mathematics, literature, and beyond. Each course is a constellation waiting to guide you through the intricacies of its subject matter.",
    "The academic courses we offer are like a mosaic of insights and ideas. From deciphering ancient languages to engineering marvels, our courses encapsulate the brilliance of human understanding. Join us in the journey of discovery.",
    "Academic excellence meets exploration in our course offerings. Embark on a mission to comprehend the complexities of life, the universe, and everything in between. Our courses are designed to challenge your intellect and broaden your horizons.",
    "Elevate your intellect with our academic courses that span the tapestry of human knowledge. Traverse the landscapes of philosophy, mathematics, history, and innovation. As you embark on your academic journey, you'll uncover the layers of insight that enrich your perspective.",
    "Our academic courses are like chapters in the book of human understanding. From the pages of mathematics to the verses of literature, each course contributes to the story of learning. Immerse yourself in the narrative and become a protagonist in your educational journey.",
    "quit",
]


def qa(_question):
    for _res in sample_responses:
        yield _res
        sleep(randint(1, 5))


app = Flask(__name__)

@app.route('/courseInfo', methods=['POST'])
def handle_question():
    data = request.get_json()  # Assuming the question is sent as a JSON payload
    question = data['question']
    
    # Return the answer as a JSON response
    return Response(qa(question), mimetype='text/plain')


if __name__ == '__main__':
    print('Spinning Servers')
    app.run(host='0.0.0.0', port=8891)