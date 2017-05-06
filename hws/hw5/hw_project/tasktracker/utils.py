from datetime import date
from datetime import timedelta


class TASK_STATES:
    in_progress = "in progress"
    ready = "ready"

CRITICAL_DAYS_FAIL = timedelta(days=3)


class IsFailed:

    def __get__(self, obj, type=None):
        return True if obj.state == TASK_STATES.in_progress and obj.estimate < date.today() else False

    def __set__(self, obj, value):
        raise AttributeError

    def __delete__(self, instance):
        raise AttributeError


class Task:

    is_failed = IsFailed()

    def __init__(self, title='', estimate=None, state=TASK_STATES.in_progress):
        self.title = title
        self.state = state
        self.estimate = date.today() if estimate is None else estimate

    def is_critical(self):

        if self.is_failed:
            return True

        if self.state == TASK_STATES.in_progress and self.estimate - date.today() < CRITICAL_DAYS_FAIL:
            return True

        return False

# Temp Storage for tasks
CURRENT_TASKS = []

