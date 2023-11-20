FROM python:3.8-alpine

# set environment variables
WORKDIR /app

# install dependencies
COPY requirements.txt /app
RUN pip install -r requirements.txt

# copy project
ADD . /app/

RUN ls -la

# run server
CMD ["python","-u","booking.py"]
