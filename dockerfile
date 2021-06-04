# get python as the Docker basis
FROM python:3.8.3

# add all files in the directory to the container
ADD . .

# install other necessary libraries
RUN pip install flask
RUN pip install textacy
RUN pip install spacy
RUN pip install spacy-transformers
RUN python -m spacy download en_core_web_sm

# Expose a port for Flask
EXPOSE 5000

# set the working directory
WORKDIR /nerflask

# run flask server
CMD [ "python", "app.py" ]
