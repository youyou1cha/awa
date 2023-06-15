# coding:utf-8

import threading
import queue
import time

class MyThread:
    def __init__(self,max_num=10) -> None:
        self.queue = queue.Queue()
        for n in  range(max_num):
            self.queue.put(threading.Thread)

    def get_thread(self):
        return self.queue.get()

    def pub_thread(self):
        self.queue.put(threading.Thread)

pool = MyThread(5)
def RunThread(arg,pool):
    print(arg)
    time.sleep(2)
    pool.pub_thread()

for n in range(30):
    thread = pool.get_thread()
    t = thread(target=RunThread,args=(n,pool,))
    t.start()