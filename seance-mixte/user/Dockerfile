FROM python:3.8-alpine

# set environment variables
WORKDIR /app

# install dependencies
COPY requirements.txt /app
RUN pip install -r requirements.txt

# copy project
ADD . /app/

# generate proto files
RUN python -m grpc_tools.protoc -I=./protos --python_out=. --grpc_python_out=. booking.proto

# run server
CMD ["python","-u","user.py"]
