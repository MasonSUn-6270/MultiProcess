import time
import multiprocessing
#TODO 无

def foo():
    var = 1
    while var <= 10 ** 1:
        _ = [num for num in range(10 ** 6)]
        var += 1


def count_time(func):
    def wrapper():
        a = time.time()
        func()
        b = time.time()
        return b - a

    return wrapper


@count_time
def normal():
    foo()
    foo()


@count_time
def multi_core():
    [multiprocessing.Process(target=foo).start() for _ in range(2)]
    [process.join() for process in multiprocessing.active_children()]


if __name__ == '__main__':
    for i in range(1, 11):
        print(f'第{i}次结果: 普通与multiprocessing相差{normal() - multi_core()}s')
