from datetime import date
from datetime import timedelta


class TASK_STATES:
    in_progress = "in progress"
    ready = "ready"


class Remaining:

    def __get__(self, obj, type=None):
        return obj.estimate - date.today() if obj.state == TASK_STATES.in_progress else 0

    def __set__(self, obj, value):
        raise AttributeError

    def __delete__(self, instance):
        raise AttributeError


class IsFailed:

    def __get__(self, obj, type=None):
        return True if obj.state == TASK_STATES.in_progress and obj.estimate < date.today() else False

    def __set__(self, obj, value):
        raise AttributeError

    def __delete__(self, instance):
        raise AttributeError


class Task:
    remaining = Remaining()
    is_failed = IsFailed()

    def __init__(self, title, estimate, state=TASK_STATES.in_progress):
        self.title = title
        self.estimate = estimate
        self.state = state

    def ready(self):
        self.state = TASK_STATES.ready

    def __str__(self):
        return 'Title: {} | Estimate: {} | State: {} '.format(self.title, self.estimate, self.state)


class TodayTasks:

    def __get__(self, obj, type=None):
        return [task for task in obj.tasks if task.estimate == date.today()]

    def __set__(self, obj, value):
        raise AttributeError

    def __delete__(self, instance):
        raise AttributeError


class RoadMap:
    today = TodayTasks()

    def __init__(self, tasks=list()):
        self.tasks = tasks

    def filter(self, state):
        return [task for task in self.tasks if task.state == state]


if __name__ == '__main__':

    today = date.today()
    tdm1 = timedelta(days=1)

    # Task
    t1 = Task('get job', today)
    print(t1.remaining)
    print(t1.is_failed)

    t2 = Task('save world', today+tdm1)
    print(t2.remaining)
    print(t2.is_failed)

    t3 = Task('save world', today-tdm1)
    print(t3.remaining)
    print(t3.is_failed)

    #Road map
    tl = list()
    tl.append(Task('1', today))
    tl.append(Task('2', today))
    tl.append(Task('3', today-tdm1))
    tl.append(Task('4', today-tdm1))
    t5 = Task('5', today-tdm1)
    t5.ready()
    tl.append(t5)

    rm0 = RoadMap()
    for t in tl:
        rm0.tasks.append(t)

    print()
    for t in rm0.today:
        print(t)

    print()
    for t in rm0.filter(TASK_STATES.ready):
        print(t)

    print()
    for t in rm0.filter(TASK_STATES.in_progress):
        print(t)


    rm1 = RoadMap(tl)
    print()
    for t in rm1.today:
        print(t)

    print()
    for t in rm1.filter(TASK_STATES.ready):
        print(t)

    print()
    for t in rm1.filter(TASK_STATES.in_progress):
        print(t)

