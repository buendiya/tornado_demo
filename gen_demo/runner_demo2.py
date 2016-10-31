# encoding=utf-8
"""
输出：
False
function_2 finish
True
function finish

说明：
在用coroutine调用过程中，只要下层返回的future的_done都是False, 则上层调用栈中yield返回的future的_done也都是False的;
同时因为如下代码:
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
            # 结束 running
            return

    def handle_yield(self, yielded):
        ...
        if not self.future.done() or self.future is moment:
            # 将当前的running循环加入到ioloop回调，直到future的_done变为True
            self.io_loop.add_future(
                self.future, lambda f: self.run())
            return False
        return True

导致当前的调用Runner暂停; 直到下层返回的future的_done变为True，下层的Runner重新开始执行;
下层的Runner执行完成之后，会将result_future(即下层返回给上层的future)置为done；
    def run(self):
        try:
            self.running = True
            while True:
                    yielded = self.gen.send(value)
                except (StopIteration, Return) as e:
                    ...
                    self.result_future.set_result(_value_from_stopiteration(e))
                    ...
                    return
            ...

下层的Runner无论是否结束,是否是重新running，其返回给上层的future是唯一的，都是按如下调用生成的future
def _make_coroutine_wrapper(func, replace_callback):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        future = TracebackFuture()

在第一次执行时，下层返回给上层的这个future是undone的，上层用这个future设置done回调：
当下层重新running结束后，会将future置为done，然后上层设置的done回调（即self.run)接着执行
"""

from tornado import gen
from tornado.concurrent import Future
from tornado.ioloop import IOLoop


future_not_done = Future()
future_is_done = Future()
future_is_done._done = True


@gen.coroutine
def sub_function():
    yield future_is_done
    yield future_not_done


@gen.coroutine
def function():
    yield sub_function()
    print 'function finish'


@gen.coroutine
def sub_function_2():
    yield future_is_done


@gen.coroutine
def function_2():
    yield sub_function_2()
    print 'function_2 finish'


if __name__ == '__main__':
    future = function()
    print future.done()

    future_2 = function_2()
    print future_2.done()

    # or future_not_done.set_result('any value')
    future_not_done._set_done()

    IOLoop.current().start()
