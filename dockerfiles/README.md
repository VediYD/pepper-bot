## About 
The Pepper Bot Docker image provides an environment for developers to run Python commands to make the Pepper robot perform various actions supported by the Python SDK.
Given below is version information,
1. Python Image: 2.7
2. Python SDK version: [2.5.10](https://www.aldebaran.com/en/support/pepper-naoqi-2-9/downloads-softwares)

## Installation

To use this image, you'll need to have Docker installed on your machine. Once you have Docker installed, you can build the Docker image using the provided Dockerfile. 

```
docker build -t pepper-bot-dev:latest -f Dockerfile.01 .
```
NOTE: make sure to run this command from `pepper-bot/dockerfiles/` folder. Or if youre in the project root pass `-f dockerfiles/Dockerfile.01`. From outside the repository pass the full path `-f /full/path/to/Dockerfile.01` 
This will create a Docker image with the Pepper Bot application and all dependencies.

## Usage

To run Pepper Bot, you can start a container using the Docker image:

```
docker run -p 8888:8888 -v /path/to/notebooks:/app pepper-bot-dev:latest
```
NOTE: A notebook has also been added to the project root for testing. 

This will start a container with the jupyter notebook running. From there, you can open it in the browser by copying the url presented [run commands](http://doc.aldebaran.com/2-1/dev/python/tutorials.html).

## Jupyter Version
In the future, we plan to release a Jupyter version of the Pepper Bot Docker image. Stay tuned for more information!

## Contributing

If you would like to contribute to Pepper Bot, feel free to fork the repository and submit a pull request. 

## License

Pepper Bot is released under the MIT license. See LICENSE file for more details.

---
The file above was generated using ChatGPT on https://chat.openai.com/ on 11th May 2023. The prompt included "create readme for this project ... <outputs from ls, and cat Dockerfile.01>"
