# API-MIX

## Description
This project consists of several microservices that collectively manage a movie booking system. Each microservice is 
contained within a separate directory

## Microservices

### 1. Booking Service
The booking service is responsible for managing the booking of tickets for movies. It is implemented using a *gRPC* 
server and client based on the *protobuf* definition both implemented in *Python*. It have a direct access to time service

- `booking/Dockerfile`: Containerization of the booking service
- `booking/booking.py`: Implementation of the booking service server/client
- `booking/proto/`: Directory containing Protobuf definitions for communication.
- `booking/requirements.txt`: Python dependencies for the booking service
- `booking/data/bookings.json`: JSON file containing booking data.

### 2. Movie Service
The movie service is responsible for managing the movies that are available in the system. It is implemented using a
*GraphQL* server and client based on the *GraphQL* definition both implemented in *Python*.

- `movie/Dockerfile`: Containerization of the movie service
- `movie/movie.py`: Implementation of the movie service server
- `movie/movie.graphql`: GraphQL schema for the Movie service.
- `movie/requirements.txt`: Python dependencies for the movie service
- `movie/data/movies.json`: JSON file containing movie data.
- `movie/data/actors.json`: JSON file containing actor data.

### 3. Time Service
The time service is responsible for managing the time slots that are available for booking. It is implemented using a
*gRPC* server based on the *protobuf* definition implemented in *Python*.

- `showtime/Dockerfile`: Containerization of the time service
- `showtime/times.py`: Implementation of the time service server
- `showtime/proto/`: Directory containing Protobuf definitions for communication.
- `showtime/requirements.txt`: Python dependencies for the time service
- `showtime/data/times.json`: JSON file containing time data.

### 4. User Service
It is the entry point for the user to interact with the system. It is implemented using a *REST* server based on the
*OpenAPI* definition implemented in *Python*. It have a direct access to movie and booking services and indirect access
to time service.

- `user/Dockerfile`: Containerization of the user service
- `user/user.py`: Implementation of the user service server
- `user/user.yaml`: OpenAPI definition for the user service.
- `user/requirements.txt`: Python dependencies for the user service
- `user/data/users.json`: JSON file containing user data.

Since the user service has direct access to the movie and booking services, we can perform operations that modify the state of these services (add, update, delete).

And since it doesn't have direct access to the times service, it can't perform any operation that directly modifies the state of showtimes. This is why we only perform data retrieval operations indirectly (via the booking service) when our entry point is user.

## Installation

Requirements:
- Docker
- Docker Compose
- Python 3.8
- pip

### 1. Clone the repository into your local machine

- ssh:
```shell
git clone
```
- https:
```shell
git clone
```

### 2. MakeFile commands
You can use the Makefile to interact with the project. The following commands are available:

- `help`: Display the current help message.
- `build`: Build the project.
- `start`: Start the project.
- `restart`: Restart the project.
- `clean`: Clean the project.
- `start-%`: Start a specific service.
- `stop-%`: Stop a specific service.
- `restart-%`: Restart a specific service.

To use these commands, run `make <command>` in the project root directory.

## Launch the project

For testing purposes, you can use the `make start` command to start the project. This will start all the services and
expose the user service on port 3004 of your machine and it OpenAPI documentation on port 8080.
