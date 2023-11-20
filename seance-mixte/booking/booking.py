import json
from concurrent import futures

import booking_pb2_grpc
import booking_pb2
import grpc


class BookingServicer(booking_pb2_grpc.BookingServicer):

    def __init__(self):
        with open('{}/data/bookings.json'.format("."), "r") as jsf:
            self.db = json.load(jsf)["bookings"]

    def GetBookings(self, request, context):
        booking_list = booking_pb2.BookingList()
        for booking in self.db:
            booking_list.bookings.extend([self._buildBookinData(booking)])
        return booking_list

    def GetBookingByUserId(self, request, context):
        for booking in self.db:
            userid = request.userid

            if booking["userid"] == userid:
                return self._buildBookinData(booking)
        return booking_pb2.BookingData()

    def AddBooking(self, request, context):
        # Check if is already in the db
        for booking in self.db:
            if booking["userid"] == request.userid:

                # Check if date is already in the db
                for date in booking["dates"]:
                    if date["date"] == request.date:
                        date["movies"].extend(request.movies)
                        return self._buildBookinData(booking)
                booking["dates"].extend([{"date": request.date, "movies": request.movies}])
                return self._buildBookinData(booking)
        # If not, add it
        self.db.extend([{"userid": request.userid, "dates": [{"date": request.date, "movies": request.movies}]}])
        return self._buildBookinData(self.db[-1])

    @staticmethod
    def _buildBookinData(booking):
        booking_data = booking_pb2.BookingData()
        booking_data.userid = booking["userid"]
        for date in booking["dates"]:
            booking_date = booking_pb2.BookingDate()
            booking_date.date = date["date"]
            booking_date.movies.extend(date["movies"])
            booking_data.dates.extend([booking_date])
        return booking_data


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    booking_pb2_grpc.add_BookingServicer_to_server(BookingServicer(), server)
    server.add_insecure_port('[::]:3002')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
