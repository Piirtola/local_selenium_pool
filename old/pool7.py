from multiprocessing import Process, Pool, JoinableQueue, cpu_count

from queue import Empty
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class Worker(Process):
    """ Thread executing tasks from a given tasks queue """
    def __init__(self, queue):
        super(Worker, self).__init__()
        self.queue = queue
        self.driver = None

    def create_driver(self):
        if self.driver is None:
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            self.driver = webdriver.Chrome(chrome_options=chrome_options)

    def run(self):

        self.create_driver()

        while True:
            try:
                items = self.queue.get(timeout=5)
            except Empty:
                print('quitting')
                self.driver.quit()
                return

            func = items[0]
            args = items[1:]
            try:
                func(self.driver, *args)
                print(self.ident)
            except Exception as e:
                # An exception happened in this thread
                print(e)
            finally:
                # Mark this task as done, whether an exception happened or not
                self.queue.task_done()


def get_url(driver, url):

    print('getting url {}'.format(url))
    driver.get(url)

def get_data():
    with open('misc.csv', 'r') as f:
        reader = csv.reader(f)
        your_list = list(reader)
    urls = [x[0] for x in your_list]
    return urls

if __name__ == "__main__":
    urls = get_data()

    url_queue = JoinableQueue()
    workers=[]
    for i in range(cpu_count()):
        workers.append(Worker(url_queue).start())

    pool = Pool()

    for url in urls:
        url_queue.put((get_url, url))

    print('done putting')

    url_queue.join()

    print('joined')




