from wsgiref.simple_server import make_server

from datetime import date
from datetime import timedelta

from hws.hw4.parse import get_dataset
from hws.hw3.hw import Task
from hws.hw3.hw import TASK_STATES


DATASET_FILENAME = 'dataset.yml'
CRITICAL_DAYS_FAIL = timedelta(days=3)


class WSGICriticalTasks:

    def __init__(self, environment, start_response):
        self.environment = environment
        self.start_response = start_response
        self.headers = [
            ('Content-type', 'text/plain; charset=utf-8'),
        ]

    def __iter__(self):
        tasks = get_dataset(DATASET_FILENAME)

        if tasks:
            self.ok_response()
            for task in tasks:
                task = Task(task[0], task[2], task[1])

                if is_critical(task):
                    yield '{}\n'.format(task).encode()
        else:
            self.no_content_response()

    def ok_response(self):
        self.start_response('200 OK', self.headers)

    def no_content_response(self):
        self.start_response('204 No Content', self.headers)


def is_critical(task):

    if task.is_failed:
        return True

    if task.state == TASK_STATES.in_progress and task.estimate - date.today() < CRITICAL_DAYS_FAIL:
        return True

    return False


if __name__ == '__main__':

    srv = make_server('127.0.0.1', 80, WSGICriticalTasks)
    srv.serve_forever()
