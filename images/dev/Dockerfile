
FROM python:3.12.1-bullseye

WORKDIR /root/project

RUN apt-get -y update  && apt-get -y upgrade

# Install make
RUN apt-get -y install make

RUN pip install pip-tools

RUN pip install --upgrade pip

COPY requirements.txt /tmp/requirements.txt

RUN pip install -r /tmp/requirements.txt

ENV PYTHONPATH "/root/project/"

ENTRYPOINT ["jupyter", "lab","--ip=0.0.0.0", "--port=8080","--allow-root"]