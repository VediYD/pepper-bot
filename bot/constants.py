"""
#1: prompts

#2: fileTransfer
### otherPackages: paramiko, 
### constants: PEPPER_RECORDINGS_PATH, SERVER_RECORDINGS_PATH, PEPPER_HOST

#3: displayGeneration
### otherPackages: shutil, pd, fileinput
### constants: FILE_NAME_TEMP, TEXT_BY_ID_PATH, PEPPER_QR_LANDING, PEPPER_IMG_LANDING, PEPPER_PAGE_LANDING
### dependencies: fileTransfer
from fileTransfer import sendFileToPepper, showPage

#4: interactiveControls
### otherPackages: ALProxy, time, threading
### constants: PEPPER_HOST, PEPPER_PORT, PEPPER_PAGE_LANDING
### dependencies: displayGeneration
from displayGeneration import generateDefaultPage, generateDashLoader, generateWelcomePage, generateStudyPage, generateUpperCoursePage, generateAccomodationPage, generateClubPage, generateCampusPage
from fileTransfer import sendToPepper,

#5: idle
### otherPackages: ALProxy, time, threading
### constants: PEPPER_HOST, PEPPER_PORT
### dependencies:

#6: humanInteraction
### otherPackages: ALProxy, requests, time, sr, threading, os, random
### constants: PEPPER_HOST, PEPPER_PORT
### dependencies: fileTransfer, interactiveControls, prompts
from fileTransfer import sendFromPepper, 
from interactiveControls import showWhichPage, resetEyesAndTablet, set_leds
import prompts
"""

global GPT_HOST, GPT_PORT, PEPPER_HOST, PEPPER_PORT, PEPPER_RECORDINGS_PATH, SERVER_RECORDINGS_PATH, PEPPER_HTML_PATH, PEPPER_PAGE_LANDING, PEPPER_QR_LANDING, PEPPER_IMG_LANDING, TEXT_BY_ID_PATH

### Naoqi Related Imports ###
import naoqi
from naoqi import qi
from naoqi import ALProxy

### System Related Imports ###
import fileinput, os, shutil, sys, random, threading, time

### Flask Related Imports ###
import json, requests

### Speech Recognition Imports ###
import pandas as pd
import paramiko
import speech_recognition as sr

### Networking Constants ###
GPT_HOST = "10.104.23.208"
PEPPER_HOST = "10.104.23.185"
GPT_PORT = 8891
PEPPER_PORT = 9559
GPT_LINK = "http://10.104.23.130:8891" # 'http://10.104.22.24:8891'

### Audio Processing Constants ###
PEPPER_RECORDINGS_PATH = "/home/nao/microphones/recording.wav"
SERVER_RECORDINGS_PATH = "recordings/recording.wav"

### Display Generation Constants ###
FILE_NAME_TEMP = "display.html"
PEPPER_HTML_PATH = "/home/nao/.local/share/PackageManager/apps/robot-page/html/"  # page.html"
PEPPER_PAGE_LANDING = PEPPER_HTML_PATH + "page.html" # '/home/nao/.local/share/PackageManager/apps/robot-page/html/page.html'
PEPPER_QR_LANDING = PEPPER_HTML_PATH + "webfiles/qr.png"  # switched slash direction
PEPPER_IMG_LANDING = PEPPER_HTML_PATH + "webfiles/img.png"  # switched slash direction
TEXT_BY_ID_PATH = "textbyID.csv"

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

combinedTopicPrompts = [
    "Deakin offers a wide range of courses across different disciplines and levels. What are you interested in studying?",
    "Deakin is a leading university in research and innovation, with many opportunities for students to get involved. Are you curious about our research areas and projects?",
    "Deakin has a vibrant and diverse student community, with many clubs, societies and events to enjoy. Would you like to hear about activities?",
    "Deakin has four campuses across Victoria, each with its own unique features and facilities. Which campus are you planning to visit or study at?",
    "Deakin has a flexible and supportive learning environment, with many options for online and blended delivery. How do you prefer to learn and study?"
]