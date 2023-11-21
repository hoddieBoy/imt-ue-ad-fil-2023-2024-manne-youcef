import json
from concurrent import futures

import booking_pb2_grpc
import booking_pb2
import showtime_pb2
import showtime_pb2_grpc
import grpc


class BookingServicer(booking_pb2_grpc.BookingServicer):

    def __init__(self):
        with open('{}/data/bookings.json'.format("."), "r") as jsf:
            self.db = json.load(jsf)["bookings"]

    def GetBookings(self, request, context) -> booking_pb2.BookingList:
        """
        Retrieve a list of all bookings.

        Parameters
        ----------
        :param request: Empty gRPC request
        :param context: gRPC context

        :return: A list of all bookings
        """
        booking_list = booking_pb2.BookingList()
        for booking in self.db:
            booking_list.bookings.extend([self._buildBookinData(booking)])
        return booking_list

    def GetBookingByUserId(self, request, context):
        """
        Retrieve booking details for a specific user.

        Parameters
        ----------
        :param request: gRPC request containing the user id
        :param context: gRPC context
        :return:
        """
        for booking in self.db:
            userid = request.userid

            if booking["userid"] == userid:
                return self._buildBookinData(booking)

        return booking_pb2.BookingData()

    def AddBooking(self, request, context):
        """
        Add a booking for a specific user.

        :param request: gRPC request containing the user id, the date and the movie
        :param context: gRPC context
        :return:
        """
        # Check if is already in the db
        for booking in self.db:
            if booking["userid"] == request.userid:

                # Check if date is already in the db
                for date in booking["dates"]:
                    if date["date"] == request.date:
                        date["movies"].extend(request.movie)
                        return self._buildBookinData(booking)
                channel = grpc.insecure_channel('showtime:3003')
                stub = showtime_pb2_grpc.ShowTimeStub(channel)
                response = stub.GetScheduleByDate(showtime_pb2.Date(date=request.date))

                if len(response.movies) == 0:
                    return booking_pb2.BookingData()

                booking["dates"].extend([{"date": request.date, "movies": [request.movie]}])
                return self._buildBookinData(booking)
        # If not, add it
        self.db.extend([{"userid": request.userid, "dates": [{"date": request.date, "movies": [request.movie]}]}])
        return self._buildBookinData(self.db[-1])

    @staticmethod
    def _buildBookinData(booking):
        """
        Build a BookingData gRPC message from a booking dict.

        Parameters
        ----------
        :param booking: a dict containing the booking data
        :return: a BookingData gRPC message
        """
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
