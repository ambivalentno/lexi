import time
import urllib2
from multiprocessing.dummy import Pool as ThreadPool
from multiprocessing import Queue
# from .models import DownLink, DownProcess


def url_generator():
    urls = [
        'http://www.google.com',
        'http://www.python.org',
        'http://www.python.org/about/',
        'https://www.python.org/downloads/',
        'https://www.python.org/doc/',
        'https://www.python.org/community/',
        'http://www.google.com',
        'http://www.python.org',
        'http://www.python.org/about/',
        'https://www.python.org/downloads/',
        'https://www.python.org/doc/',
        'https://www.python.org/community/',
    ]
    urls += urls
    for url in urls:
        yield url


def f_init(q):
    f.q = q

def f(url):
    result = urllib2.urlopen(url)
    f.q.put(result.getcode())
    return


queue = Queue()
pool = ThreadPool(4, f_init, [queue])

start = time.time()
pool.map(f, url_generator())
pool.close()

for res in queue.get():
    print res

end = time.time() - start

print end

http://docs.python.org/2/library/multiprocessing.html#exchanging-objects-between-processes
