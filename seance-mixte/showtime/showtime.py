import json
from concurrent import futures

import grpc

import showtime_pb2
import showtime_pb2_grpc


class ShowtimeServicer(showtime_pb2_grpc.ShowTimeServicer):

    def __init__(self):
        with open('{}/data/times.json'.format("."), "r") as jsf:
            self.db = json.load(jsf)["schedule"]

    def GetAllSchedule(self, request, context) -> showtime_pb2.ScheduleList:
        """
        Retrieve a list of all schedule.

        Parameters
        ----------
        :param request: Empty gRPC request
        :param context: gRPC context

        :return: A list of all schedule
        """
        Schedule = showtime_pb2.ScheduleList()
        for schedule in self.db:
            Schedule.schedule.append(self._build_schedule(schedule))
        return Schedule

    def GetScheduleByDate(self, request, context) -> showtime_pb2.ScheduleItem:
        """
        Retrieve schedule details for a specific date.

        Parameters
        ----------
        :param request: gRPC request containing the date
        :param context: gRPC context
        :return: a schedule for a specific date
        """
        for schedule in self.db:
            if schedule["date"] == request.date:
                return self._build_schedule(schedule)
        return showtime_pb2.ScheduleItem()

    @staticmethod
    def _build_schedule(schedule: dict) -> showtime_pb2.ScheduleItem:
        """
        Build a schedule from a dictionary.

        :param schedule: a dictionary containing the schedule
        :return:
        """
        scheduleItem = showtime_pb2.ScheduleItem(date=schedule["date"])
        for time in schedule["movies"]:
            scheduleItem.movies.append(time)
        return scheduleItem




def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    showtime_pb2_grpc.add_ShowTimeServicer_to_server(ShowtimeServicer(), server)
    server.add_insecure_port('[::]:3003')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
