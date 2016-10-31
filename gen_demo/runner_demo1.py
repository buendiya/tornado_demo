# encoding=utf-8
"""

说明：
由于Runner class，在用coroutine调用过程中，只要所有yield返回的future的_done都是True, 整个调用过程会自动完成;
同时因为如下代码:

def _make_coroutine_wrapper(func, replace_callback):
    ...
    _futures_to_runners[future] = Runner(result, future, yielded)
    ...

class Runner(object):
    def __init__(self, gen, result_future, first_yielded):
        ...
        if self.handle_yield(first_yielded):
            self.run()

    def run(self):
        ...
        yielded = self.gen.send(value)
        ...
        if not self.handle_yield(yielded):
            return

    def handle_yield(self, yielded):
        ...
        if not self.future.done() or self.future is moment:
            self.io_loop.add_future(
                self.future, lambda f: self.run())
            return False
        return True

"""

from tornado import gen
from tornado.concurrent import Future


@gen.coroutine
def sub_function():
    for i in range(2):
        future_is_done = Future()
        future_is_done.set_result(i)
        res = yield future_is_done
        print 'sub_function %s' % res


@gen.coroutine
def function():
    for _ in range(2):
        yield sub_function()
        print 'function'


if __name__ == '__main__':
    future = function()
    print future.done()
