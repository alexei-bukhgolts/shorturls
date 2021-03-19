FROM python:3.9

ENV PYTHONUNBUFFERED 1

RUN mkdir /shorturls

WORKDIR /shorturls

ADD . /shorturls/

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt