import json
from concurrent import futures

import booking_pb2_grpc
import booking_pb2
import grpc


class BookingServicer(booking_pb2_grpc.BookingServicer):

    def __init__(self):
        with open('{}/data/bookings.json'.format("."), "r") as jsf:
            self.db = json.load(jsf)["schedule"]

    def GetBookings(self, request, context):
        for booking in self.db:
            yield booking_pb2.BookingData(userid=booking["userid"], dates=booking["dates"])


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    booking_pb2_grpc.add_BookingServicer_to_server(BookingServicer(), server)
    server.add_insecure_port('[::]:3002')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
