# Get the bitnami spark image
FROM bitnami/spark:latest
USER root
# Install Python libraries 
COPY requirements.txt requirements.txt
ARG src="Alldata_refined.csv" 
COPY ${src} /opt/bitnami/spark/alldata_refined.csv 
RUN apt-get update && apt-get install -y curl
RUN apt install build-essential -y
RUN apt install libpq-dev python-dev -y
RUN pip install -r requirements.txt
RUN python -m pip install -U pydantic spacy
RUN python -m spacy download en_core_web_sm
RUN [ "python", "-c", "import nltk; nltk.download('wordnet')" ]
RUN [ "python", "-c", "import nltk; nltk.download('vader_lexicon')" ]
RUN apt update -y
