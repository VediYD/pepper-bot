## About 
The Pepper Bot Docker image provides an environment for developers to run Python commands to make the Pepper robot perform various actions supported by the Python SDK.
Given below is version information,
1. Python Image: 2.7
2. Python SDK version: [2.5.10](https://www.aldebaran.com/en/support/pepper-naoqi-2-9/downloads-softwares)

## Installation

To use this image, you'll need to have Docker installed on your machine. Once you have Docker installed, you can build the Docker image using the provided Dockerfile. 

```
docker build -t pepper-bot-dev:latest .
```

This will create a Docker image with the Pepper Bot application and all dependencies.

## Usage

To run Pepper Bot, you can start a container using the Docker image:

```
docker run -it pepper-bot-dev:latest
```

This will start a container with the Pepper Bot application running. From there, you can start a python terminal and [run commands](http://doc.aldebaran.com/2-1/dev/python/tutorials.html).

## Jupyter Version
In the future, we plan to release a Jupyter version of the Pepper Bot Docker image. Stay tuned for more information!

## Contributing

If you would like to contribute to Pepper Bot, feel free to fork the repository and submit a pull request. 

## License

Pepper Bot is released under the MIT license. See LICENSE file for more details.

---
The file above was generated using ChatGPT on https://chat.openai.com/ on 11th May 2023. The prompt included "create readme for this project ... <outputs from ls, and cat Dockerfile.01>"
