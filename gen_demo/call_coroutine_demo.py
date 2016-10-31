
import logging

from tornado import gen
from tornado.ioloop import IOLoop
from tornado.httpclient import AsyncHTTPClient


logging.basicConfig()

http_client = AsyncHTTPClient()


@gen.coroutine
def divide(x, y):
    return x / y


def bad_call():
    # This should raise a ZeroDivisionError, but it won't because
    # the coroutine is called incorrectly.
    divide(1, 0)


def callback(*args, **kwargs):
    print 'callback is called', args, kwargs


@gen.coroutine
def good_call():
    # yield will unwrap the Future returned by divide() and raise
    # the exception.

    for i in range(10):
        res = yield divide(i, 0)
        print res
    raise gen.Return("hi, I am good_call's return")
        # yield 1


def ioloop_call():
    # The IOLoop will catch the exception and print a stack trace in
    # the logs. Note that this doesn't look like a normal call, since
    # we pass the function object to be called by the IOLoop.
    return IOLoop.current().spawn_callback(divide, 1, 0)


def ioloop_call2():
    # run_sync() doesn't take arguments, so we must wrap the
    # call in a lambda.
    IOLoop.current().run_sync(lambda: divide(1, 0))


if __name__ == '__main__':
    pass
#     print bad_call()

    future = good_call(callback=callback)
    print future.__dict__

#     IOLoop.current().start()

#     print ioloop_call2()


