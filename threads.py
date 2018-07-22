from threading import Thread
import Queue
from time import sleep

class ListShare(object):
    def __init__(self):
        self.ls = list()

    def add(self, value):
        if value not in self.ls:
            self.ls.append(value)

    def get_length(self):
        return len(self.ls)

    def get(self):
        if self.ls:
            return self.ls.pop()
        else:
            return None

class ScanQue(Thread):
    def __init__(self):
        self.ls = ListShare()
        self.queue = Queue.Queue()
        self.end = False
        self.end_run = True
        self.counter = 0
        self.last_send = False

    def send_url(self, url):
        self.ls = url

    def func_to_run(self, url, queue,func):
        res = func(url)
        if res > 0:
            queue.put(1)

    def run_process(self, func,limit= 100):
        threads = []
        while not self.end:
            value = self.ls.get()
            if len(threads) < limit and value:
                t = Thread(target=self.func_to_run, args=tuple([value, self.queue, func]))
                t.start()
                threads.append(t)
                self.counter += 1
            else:
                for t in threads:
                    t.join()
                threads = list()
            if value is None and self.last_send and len(threads) == 0:
                end_result = self.end_process()
            #sleep(0.1)


    def end_process(self):
        self.end = True
        ls = []
        while not self.queue.empty():
            ls.append(self.queue.get())
        self.result = len(ls)




