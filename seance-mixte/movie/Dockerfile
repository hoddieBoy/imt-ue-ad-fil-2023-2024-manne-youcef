FROM --platform=linux/x86_64 python:3.8-alpine

# set environment variables
WORKDIR /app

# install dependencies
COPY requirements.txt /app
RUN pip install -r requirements.txt

# copy project
ADD . /app/

# run graphql server
CMD ["python","-u","movie.py"]
