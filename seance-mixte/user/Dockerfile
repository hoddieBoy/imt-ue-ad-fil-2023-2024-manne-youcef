FROM python:3.8-alpine
# set environment variables
WORKDIR /app

# install dependencies
COPY requirements.txt /app
RUN pip install -r requirements.txt

# copy project
ADD . /app/

# run server
CMD ["python","-u","user.py"]
