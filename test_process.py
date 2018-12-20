from multiprocessing import Process, Manager
from threading import Thread
from test import dt,lt

def func():
    global dt,lt
    for i in range(10):
        key = 'arg' + str(i)
        dt[key] = i * i

    lt += range(11, 16)


if __name__ == "__main__":

    print(id(dt))
    print(id(lt))
    t = Thread(target=func)
    t.start()
    t.join()
    print dt, '\n', lt
    print(id(dt))
    print(id(lt))
