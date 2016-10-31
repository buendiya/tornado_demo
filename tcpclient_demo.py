# encoding=utf-8
"""
必须用IOLoop， 因为要监听read；

也需要用到gen.coroutine.
因为第一次尝试read时，可能tcpserver还没有响应，iostream的_read_future就会是undone的，coroutine也就会卡在这儿；
tcpserver响应之后，会回调到iostream的_handle_events -> _handle_read, 读取完成之后，会将读取到的数据写到_read_future，
此时_read_future当然也变为done, coroutine会继续运行
"""
from tornado import gen
from tornado.ioloop import IOLoop
from tornado.tcpclient import TCPClient

stream = None


def out(data):
    print(data)
    IOLoop.current().stop()


@gen.coroutine
def setup():
    global stream
    stream = yield TCPClient().connect("localhost", 8888)
    stream.write(b"hello, world\n")
    stream.read_until(b"\n", callback=out)
    # or could call out() with empty data, to save duplication


@gen.coroutine
def setup_2():
    global stream
    stream = yield TCPClient().connect("localhost", 8888)
    stream.write(b"hello, world\n")
    data = yield stream.read_until(b"\n")
    print data
    IOLoop.current().stop()

if __name__ == '__main__':
    setup_2()
    # setup()
    IOLoop.current().start()
