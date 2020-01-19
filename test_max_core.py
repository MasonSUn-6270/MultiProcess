import multiprocessing
import time
from speedtest import foo
import matplotlib.pyplot as plt
from functools import wraps



def count_time(func):
    @wraps(func)
    def wrapper(t):
        a = time.time()
        func(t)
        b = time.time()
        return b - a

    return wrapper


@count_time
def run(core_num):
    [multiprocessing.Process(target=foo).start() for _ in range(core_num)]
    print(f'active_children_num : {len(multiprocessing.active_children())}')
    [process.join() for process in multiprocessing.active_children()]


@count_time
def normal(time_):
    var_a = 1
    while var_a <= time_:
        foo()
        var_a += 1


def collect_data(max) -> dict:
    data = {}
    for func in [run, normal]:
        print(func.__name__)
        data[func.__name__] = {}
        for i in range(1, max + 1, 5):
            spend_time = func(i)
            data[func.__name__][i] = spend_time
    return data


if __name__ == '__main__':
    data = collect_data(20)
    [plt.plot(list(data[i].keys()), list(data[i].values()), label='multi') for i in data.keys()]
    plt.legend()
    plt.xlabel('process NUM')
    plt.ylabel('second spend')
    plt.tight_layout()
    plt.show()
