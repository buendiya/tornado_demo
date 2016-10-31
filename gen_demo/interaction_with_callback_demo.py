"""
To interact with asynchronous code that uses callbacks instead of Future, wrap the call in a Task.
This will add the callback argument for you and return a Future which you can yield:
"""

import logging

from tornado import gen

logging.basicConfig()


def call_back(myargument, callback):
    print 'callback is called', myargument, callback
    callback(myargument)
    raise gen.Return(myargument)


@gen.coroutine
def call_task():
    # Note that there are no parens on some_function.
    # This will be translated by Task into
    #   some_function(other_args, callback=callback)
    yield gen.Task(call_back, 'Hi')


if __name__ == '__main__':
    pass
    future = call_task()
    print future.__dict__
