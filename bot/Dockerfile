FROM python:2.7

RUN wget https://community-static.aldebaran.com/resources/2.5.10/Python%20SDK/pynaoqi-python2.7-2.5.7.1-linux64.tar.gz

RUN tar -xzf pynaoqi-python2.7-2.5.7.1-linux64.tar.gz -C / \
    && rm pynaoqi-python2.7-2.5.7.1-linux64.tar.gz

ENV PYTHONPATH=${PYTHONPATH}:/pynaoqi-python2.7-2.5.7.1-linux64/lib/python2.7/site-packages
ENV PYTHONPATH=${PYTHONPATH}:/pynaoqi-python2.7-2.5.7.1-linux64

ENV LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/pynaoqi-python2.7-2.5.7.1-linux64

RUN pip install jupyter
EXPOSE 8888

WORKDIR /app

CMD ["jupyter", "notebook", "--ip", "0.0.0.0", "--no-browser", "--allow-root"]