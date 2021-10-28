# pull official base image
FROM python:3.9.7

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# # install SQLAlchemy dependencies
# RUN apk update \
# 	&& apk add --no-cache gcc g++ python3-dev unixodbc-dev

# install dependencies
RUN python -m pip install --upgrade pip setuptools wheel
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .
