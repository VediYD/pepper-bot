# Pepper Bot
Main repo for the Pepper-Bot project @ Deakin University.

# Introduction
TBA
NOTE: This document is a WIP. Watch out for future updates. 

# Quick Start
TBA

# Development Environment
To get added as a collaborator on this project, please get approval from bahar.nakisa@deakin.edu.au or hharland@deakin.edu.au. 
Note: Presently, working on this repo is only for the students studying @ Deakin University. 

## Getting Started
You will need to clone the repository to start contributing to the project. Furthermore, a docker image has been created and published to aid with the development (and eventually deployment) process involved in this project. The specific Dockerfiles used to build the image has been provided in the `/dockerfiles` folder. This folder will also have other dockerfiles used to host the code for other components of the overall project. Instructions to building the image yourself have been provided in `/dockerfiles/README.md` file.

In order to use the Dockerized development environment you need to have Docker installed on your system. More instructions for installation are given on the [official website](https://docs.docker.com/get-docker/).

Once you have cloned the repository and have docker running on your system run the following command in the root of the project to get started. 
```powershell
docker run -p 8888:8888 -v "${PWD}:/app" vediyd/pepper-bot
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
