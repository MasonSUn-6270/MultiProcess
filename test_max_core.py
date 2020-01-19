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
def multi_core(core_num):
    [multiprocessing.Process(target=foo).start() for _ in range(core_num)]
    [process.join() for process in multiprocessing.active_children()]


@count_time
def normal(time_):
    var_a = 1
    while var_a <= time_:
        foo()
        var_a += 1


def collect_data(max) -> dict:
    data = {}
    for func in [multi_core, normal]:
        data[func.__name__] = []
        [data[func.__name__].append(func(i)) for i in range(1, max + 1, 5)]
    return data


def main(num: int):
    data = collect_data(num)
    [plt.plot(list(range(1, num + 1, 5)), list(data[i]),ls='-.' ,label=i) for i in data.keys()]
    plt.legend()
    plt.title('Time to complete unit work')
    plt.xlabel('process NUM')
    plt.ylabel('second spend')
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    main(20)
