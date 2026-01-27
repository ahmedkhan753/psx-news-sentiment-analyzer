FROM ubuntu:18.04
RUN apt update
RUN apt install python3 python3-pip -y
RUN apt-get install -y update-manager python3-update-manager
RUN apt install -y  apturl
RUN apt-get install -y python-brlapi

FROM python:3.10

WORKDIR /usr/src/app

COPY start_dev.sh ./

COPY requirements.txt ./

RUN python3 -m pip install --upgrade pip
# install all dependencies listed on requirements file
RUN python3 -m pip install -r requirements.txt

# download nltk files
RUN [ "python3", "-c", "import nltk; nltk.download('stopwords')" ]
RUN [ "python3", "-c", "import nltk; nltk.download('vader_lexicon')" ]

COPY . .

EXPOSE 4200

CMD [ "sh", "./start_prod.sh" ]