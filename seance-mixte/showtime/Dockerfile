FROM python:3.8-alpine

# set environment variables
WORKDIR /app

# install dependencies
COPY requirements.txt /app

# copy project
RUN pip install -r requirements.txt
ADD . /app/

# generate proto files
RUN python -m grpc_tools.protoc -I. --python_out=./protos --grpc_python_out=. showtime.proto

# run server
CMD ["python","-u","showtime.py"]
