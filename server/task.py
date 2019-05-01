from threading import Timer
from latest_price import get_latest_price


def timed_task():
    Timer(86400, task).start()


def task():
    # Timed task
    get_latest_price()


if __name__ == '__main__':
    timed_task()
