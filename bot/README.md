# Pepper Bot
Main repo for the Pepper-Bot project @ Deakin University.

# Introduction
TBA

# Quick Start
TBA

# Development Environment
To get added as a collaborator on this project, please get approval from bahar.nakisa@deakin.edu.au or hharland@deakin.edu.au. 

Note: This project is open to contributions from Deakin University students only.

## Getting Started
You will need to clone the repository to start contributing to the project. Furthermore, a docker image has been created and published to aid with the development (and eventually deployment) process involved in this project. The specific Dockerfiles used to build the image has been provided in the `/dockerfiles` folder. This folder will also have other dockerfiles used to host the code for other components of the overall project. Instructions to building the image yourself have been provided in `/dockerfiles/README.md` file.

In order to use the Dockerized development environment you need to have Docker installed on your system. More instructions for installation are given on the [official website](https://docs.docker.com/get-docker/).

Alternatively, you may also follow the instructions for installing the Python SDK on your own machine from the official websites [here](http://doc.aldebaran.com/2-5/dev/python/install_guide.html) and [here](https://www.aldebaran.com/en/support/pepper-naoqi-2-9/downloads-softwares). If you wish to follow this approach, you can skip the docker installation entirely and the instructions below. You may start contributing directly once the SDK is installed and working.

Once you have cloned the repository and have docker running on your system run the following command in the root of the project to get started. 
```powershell
docker run -p 8888:8888 -v "${PWD}:/app" vediyd/pepper-bot
```

Or on command prompt
```cmd
docker run -p 8888:8888 -v "%cd%:/app" vediyd/pepper-bot
```
This command has been tested on both powershell and Ubuntu18.04.

The output looks like this,
```terminal
    To access the notebook, open this file in a browser:
        file:///root/.local/share/jupyter/runtime/nbserver-1-open.html
    Or copy and paste one of these URLs:
        http://(a1e4dbc53a50 or 127.0.0.1):8888/?token=a1f543ff297067fcf18323d02793d810db6ff33e762a6a62
```

After launching the docker container, you can then use the returned url to access the jupyter interface through your system's browser. 

# Useful Information for using this codebase

## String and State Definitions
### Pepper's Body Language types: 
- "loading" (was "thinking") [green eyes, tablet]
- "listening" [blue eyes, tablet]
- "confused" (was "error") [pink eyes, tablet]

### Pepper's state dict: 
- "topic" (string, describes flow position) ["fresh", "%error%" (if query[0]=="%"), "Cacc", "Club", "Camp", "Cour", "Cspe", "Cgen", "%low_volume_error%" (if query == "%low_volume_error%" in classifyQuery - should be unreachable? classifyQuery not called if query[0] == "%") 
- "confusion" (int, limits total error before quit) [0-3]
- "repeat" (bool, dictates whether the main sub-loop is repeated) [True, False]
- "confident" (bool, dictates whether confirmation is needed) [True, False]

### Pepper's default image types:
- "prompt" (with speak bubbles)
- "confused" (with pink 'sorry' pulse)
- "loading" (with green 'thinking' bubble and moving dashes)
- "listenining" (with blue 'listening' pulse)
- "Cgen" (WelcomePage, with generic image and text)
- "Cstu" (Lower banner page with some filler content)
- "Cour" (Lower banner page with some filler content)
- "Cacc" (Lower banner page with some filler content)
- "Club" (Lower banner page with some filler content)
- "Camp" (Lower banner page with some filler content)

## Module Dependencies

### 1: prompts.py

PURPOSE: to store and maintain a central reference for hardcoded quotes used by Pepper
CONTAINS: 
- combinedGreetingAndGenericPrompts(list)
- basicGreetings(list)
- basicTopicPrompts(list)
- basicCoursePrompt(list)
- courseInterlude(list)
- confusionInterlude(list)
- confusionRepeat(list)
- combinedTopicPrompts(list)
- tieredConfusionPrompts(list)
- goodbyePrompts(list)
- verificationPrompts(dict, topics)
- topicBlurb(dict, topics)
- noExamples(list)
- yesExamples(list)
PEPPER-BOT DEPENDENCIES: null
OTHER PACKAGE DEPENDENCIES: null
CONSTANT DEPENDENCIES: null
USED IN: humanInteraction.py

### 2: fileTransfer.py

PURPOSE: manages SFTP and SSH to exchange files with Pepper
CONTAINS: 
- sendFromPepper(func)
- sendToPepper(func)
- setupSFTP(func)
- closeSFTP(func)
- sendFileToPepper(func, wraps sendToPepper)
NAOQI DEPENDENCIES: username+password
PEPPER-BOT DEPENDENCIES: null
OTHER PACKAGE DEPENDENCIES: paramiko(SSHClient, AutoAddPolicy)
CONSTANT DEPENDENCIES: PEPPER_HOST, PEPPER_PORT, PEPPER_RECORDINGS_PATH, SERVER_RECORDINGS_PATH
USED IN: displayGeneration.py, interactiveControls.py, humanInteraction.py

### 3: displayGeneration.py

PURPOSE: manages creation of HTML files for Pepper's display
CONTAINS: 
- pepperLog(func)
- duplicateTemplate(func)
- seekCourseName(func)
- seekLocationText(func)
- seekHeadText(func)
- seekBodyText(func)
- seekCourseAndLocationText(func)
- seekCourseNameList(func)
- textSub(func)
- subHeadText(func)
- subBodyText(func)
- subCourseText(func)
- subLocationText(func)
- subCourseAndLocationText(func)
- subListText(func)
- seekQR(func)
- seekImg(func)
- sendPage(func)
- seekAndSend(func)
- generateBasicQRPage(func)
- generateTopBannerQRPage(func)
- generateBottomBannerQRPage(func)
- generateBottomBannerWithBodyQRPage(func)
- generateOnlyTextAndImgPage(func)
- generateBasicListViewPage(func)
- generateDashLoader(func)
- generateDefaultPage(func)
- generateListeningPage(func)
- generateErrorPage(func)
- generateWelcomePage(func)
- generateUpperCourseQRPage(func)
- generateUpperCoursePage(func, don't use)
- generateStudyPage(func)
- generateAccommodationPage(func)
- generateClubPage(func)
- generateCampusPage(func)
NAOQI DEPENDENCIES: null
PEPPER-BOT DEPENDENCIES: 
- fileTransfer[sendFileToPepper]
- textByID.txt
- QRCodes(folder of pngs)
- imgFiles(folder of pngs), pageTemplates(folder of HTMLs)
OTHER PACKAGE DEPENDENCIES: 
- bs4[BeautifulSoup]
- re[compile]
- shutil[copyfile]
- pandas[read_csv]
CONSTANT DEPENDENCIES: FILE_NAME_TEMP, TEXT_BY_ID_PATH, PEPPER_QR_LANDING, PEPPER_IMG_LANDING, PEPPER_PAGE_LANDING, PEPPER_HTML_PATH
LOCAL CONSTANTS: PATH_PREFIX, IMG_FILES_FOLDER, QR_CODES_FOLDER
USED IN: interactiveControls.py, humanInteraction.py

### 4: interactiveControls.py

PURPOSE: wrappers for controls on Pepper's behaviours, body language etc. 
CONTAINS: 
- track_head(func)
- stop_track_head(func)
- set_leds(func)
- EyesController(class)[__init__, colourEyes(method), startEyes(method), setEyes(method), stopEyes(method)]
- return_to_default_pos(func)
- defaultPosture(func)
- resetEyesAndTablet(func, tablet not implemented)
- showWhichPage(func)
- show_on_tablet(func)
- stop_show_on_tablet(func)
- showPage(func)
- hidePage(func)
NAOQI DEPENDENCIES: ALProxy
PEPPER-BOT DEPENDENCIES: 
- fileTransfer[sendToPepper]
- displayGeneration[generateDefaultPage, generateDashLoader, generateWelcomePage, generateStudyPage, generateUpperCoursePage, generateListeningPage, generateAccommosationPage, generateClubPage, generateCampusPage, generateErrorPage]
OTHER PACKAGE DEPENDENCIES: 
- threading[Thread]
- time[sleep]
CONSTANT DEPENDENCIES: PEPPER_HOST, PEPPER_PORT, PEPPER_PAGE_LANDING
LOCAL CONSTANTS: null
USED IN: humanInteraction.py

### 5: idle.py

PURPOSE: manages Pepper's idle behaviours that maintain her motors
CONTAINS: 
- idling(class)[__init__, idle_behavior_thread(method), start_idle_behaviour(method), stop(method)]
NAOQI DEPENDENCIES: ALProxy
PEPPER-BOT DEPENDENCIES: null
OTHER PACKAGE DEPENDENCIES: 
- random[choice]
- threading[Thread]git 
- time[sleep, time]
CONSTANT DEPENDENCIES: PEPPER_HOST, PEPPER_PORT
LOCAL CONSTANTS: null
USED IN: humanInteraction.py, PepperDemo.ipynb

### 6: humanInteraction.py

PURPOSE: manages Pepper's interactions with users, interactive behaviours use interactiveControls to control
CONTAINS:
- detect(func)
- listen(func)
- speak(func)
- shush(func)
- processQuery(func)
- promptForNextQuery(func)
- sayGoodbye(func)

NAOQI DEPENDENCIES: ALProxy
PEPPER-BOT DEPENDENCIES: 
- prompts[basicGreetings, basicTopicPrompts, yesExamples, verificationPrompts, confusionRepeat, tieredConfusionPrompts, topicBlurb]
- fileTransfer[sendFromPepper]
- interactiveControls[showWhichPage, set_leds, showPage]
- displayGeneration[generateBasicListViewPage, generateBasicQRPage]
OTHER PACKAGE DEPENDENCIES: 
- requests[post]
- time[time, sleep]
- random[choice]
- threading[Timer, Event, Thread]
- os.path[join]
- copy[deepcopy]
- scipy.io[wavfile]
- speech_recognition
- numpy
CONSTANT DEPENDENCIES: PEPPER_HOST, PEPPER_PORT, GPT_LINK
LOCAL CONSTANTS: link
USED IN: PepperDemo.ipynb

### 7: display.html

PURPOSE: temp file for creating and altering the htmls prior to sending to Pepper
USED IN: displayGeneration.py

### 8. constants.py

PURPOSE: stores shared constants to be altered in only one place
CONTAINS:
- 
USED IN: 


## flow for processQuery

`processQuery(query, responsesPipeline, eyes, state)`<br>
**| <br>
|--** `classifyQuery(query)`<br>
**|<br> 
|--** Case: `query` starts with "%"<br>
**|&nbsp;&nbsp;&nbsp;&nbsp;|--** Update `currentState` for confusion and repeat<br>
**|&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;|--** `showWhichPage("confused")`<br>
**|&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;|--** `eyes.setEyes("confused")`<br>
**|&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;|--** `speak(tieredConfusionPrompts[state["confusion"]])`<br>
**|&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;|--** Update `currentState` for `%error%` topic<br>
**|&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;.** <br>
**|&nbsp;&nbsp;&nbsp;&nbsp;.** <br>
**| <br>
|--** Case: `topic[:3]` in ["Acco", "Acti", "Camp"] and not confident<br>
**|&nbsp;&nbsp;&nbsp;&nbsp;|--** `verifyTopic(topic, eyes)`<br>
**|&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;|--** Verify `topic` with user and update `confident`<br>
**|&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;.** <br>
**|&nbsp;&nbsp;&nbsp;&nbsp;|--** Case: `confident` or `topic[:3]` in ["Cour", "Spec", "Gene"]<br>
**|&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;|--** Case: `topic[:3]` is "Cour" and `previousTopic` is "Cour"<br>
**|&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;|--** Set `topic` to "Spec"<br>
**|&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;.** <br>
**|&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;|--** `topicSpecificOutput(topic, query, responsesPipeline, eyes)`<br>
**|&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;|--** Case: `topicSpecificOutput` errored<br>
**|&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;|--** Update `currentState` for repetition and confusion<br>
**|&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;.** <br>
**|&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;.** <br>
**|&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;|--** Update `currentState` for repetition and confusion<br>
**|&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;.** <br>
**|&nbsp;&nbsp;&nbsp;&nbsp;|--** Case: `confident` or `topic[:3]` not met<br>
**|&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;|--** Update `currentState` for confusion<br>
**|&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;|--** `showWhichPage("confused")`<br>
**|&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;|--** `eyes.setEyes("confused")`<br>
**|&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;|--** `speak(confusionRepeat[1])`<br>
**|&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;|--** Update `currentState` for repetition<br>
**|&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;.** <br>
**|&nbsp;&nbsp;&nbsp;&nbsp;|--** Update `currentState` with `topic`<br>
**|&nbsp;&nbsp;&nbsp;&nbsp;.** <br>
**| <br>
|--** `topicSpecificOutput(topic, query, responsesPipeline, eyes)`<br>
**|&nbsp;&nbsp;&nbsp;&nbsp;|--** Case: `topic` in ["Acco", "Acti", "Camp"] and not confident<br>
**|&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;|--** `verifyTopic(topic, eyes)`<br>
**|&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;|--** Verify topic with user and update `confident`<br>
**|&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;.** <br>
**|&nbsp;&nbsp;&nbsp;&nbsp;|--** Case: `topic` is confident or "Cour", "Spec", "Gene"<br>
**|&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;|--** Case: `topic` is "Cour" and `previousTopic` is "Cour"<br>
**|&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;|--** Set `topic` to "Spec"<br>
**|&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;.** <br>
**|&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;|--** `topicSpecificOutput(topic, query, responsesPipeline, eyes)`<br>
**|&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;|--** Case: `topicSpecificOutput` errored<br>
**|&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;|--** Update `currentState` for repetition and confusion<br>
**|&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;.** <br>
**|&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;.** <br>
**|&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;|--** Update `currentState` with `topic` and confidence<br>
**|&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;.** <br>
**|&nbsp;&nbsp;&nbsp;&nbsp;|--** Case: `topic` is not confident<br>
**|&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;|--** Update `currentState` for confusion<br>
**|&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;|--** Show confusion message and update `currentState` for repetition<br>
**|&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;.** <br>
**|&nbsp;&nbsp;&nbsp;&nbsp;|--** Update `currentState` with `topic`<br>
**|&nbsp;&nbsp;&nbsp;&nbsp;.** <br>
**.**