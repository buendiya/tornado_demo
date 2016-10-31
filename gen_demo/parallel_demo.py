
import logging
import time

from tornado import gen
from tornado.httpclient import AsyncHTTPClient


logging.basicConfig()

http_client = AsyncHTTPClient()


def fetch(url):
    return http_client.fetch(url)


@gen.coroutine
def parallel_fetch_many(urls):
    yield [fetch(url) for url in urls]
    # responses is a list of HTTPResponses in the same order


if __name__ == '__main__':
    urls = ['http://www.jd.com'] * 1000
    start_time = time.time()
    parallel_fetch_many(urls)
    print 'parallel_fetch_many cost ', time.time() - start_time

    start_time = time.time()
    for url in urls:
        fetch(url)
    print 'fetch cost ', time.time() - start_time
