# -*- coding: utf-8 -*-
"""
输出：func is called

可知：func被调用了
在io_loop.start开始之后，即开始监听io，此后是没有任何io event的，但是io loop是如何调用到call_later设置的回调的？
原因在io_loop.start里：
    event_pairs = self._impl.poll(poll_timeout)

poll_timeout用来设置监听超时时间，当到达poll_timeout之后, 此次监听结束
每次监听时的poll_timeout与开始监听前设置的_callbacks和_timeouts相关，具体可以该部分代码
"""
import tornado.ioloop


def func():
    print 'func is called'


if __name__ == '__main__':
    io_loop = tornado.ioloop.IOLoop.current()
    io_loop.call_later(2, func)
    io_loop.call_later(3, io_loop.stop)
    io_loop.start()
