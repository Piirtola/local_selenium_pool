import sys
IS_PY2 = sys.version_info < (3, 0)

if IS_PY2:
    from Queue import Queue
else:
    from queue import Queue

from threading import Thread

from random import randint

class Worker(Thread):
    """ Thread executing tasks from a given tasks queue """
    def __init__(self, tasks):
        Thread.__init__(self)
        self.tasks = tasks
        self.daemon = True
        self.start()
        self.driver = self.ident

    def run(self):
        while True:
            func, args, kargs = self.tasks.get()
            try:
                func(self.driver, *args, **kargs)
                print(self.ident)
            except Exception as e:
                # An exception happened in this thread
                print(e)
            finally:
                # Mark this task as done, whether an exception happened or not
                self.tasks.task_done()


class ThreadPool:
    """ Pool of threads consuming tasks from a queue """
    def __init__(self, num_threads):
        self.tasks = Queue(num_threads)
        for _ in range(num_threads):
            Worker(self.tasks)

    def add_task(self, func, *args, **kargs):
        """ Add a task to the queue """
        self.tasks.put((func, args, kargs))

    def map(self, func, args_list):
        """ Add a list of tasks to the queue """
        for args in args_list:
            self.add_task(func, args)

    def wait_completion(self):
        """ Wait for completion of all the tasks in the queue """
        self.tasks.join()


if __name__ == "__main__":


    import csv

    with open('misc.csv', 'r') as f:
        reader = csv.reader(f)
        your_list = list(reader)


    # Function to be executed in a thread
    def get_url(driver, url):
        print(driver)
        print('getting url {}'.format(url))


    urls = [x[0] for x in your_list]

    # Generate random delays
    #delays = [randrange(1, 3) for i in range(len(urls))]

    #params = zip(delays, urls)

    # Instantiate a thread pool with 5 worker threads
    pool = ThreadPool(5)

    # Add the jobs in bulk to the thread pool. Alternatively you could use
    # `pool.add_task` to add single jobs. The code will block here, which
    # makes it possible to cancel the thread pool with an exception when
    # the currently running batch of workers is finished.
    pool.map(get_url, urls)
    pool.wait_completion()