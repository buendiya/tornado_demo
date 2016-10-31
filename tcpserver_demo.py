# encoding=utf-8
"""
发送请求时，用tcpclient，不能用浏览器，因为浏览器发送的是http请求，想要接收的也是http响应
"""
from tornado.tcpserver import TCPServer
from tornado.iostream import StreamClosedError
from tornado.ioloop import IOLoop
from tornado import gen


class EchoServer(TCPServer):
    @gen.coroutine
    def handle_stream(self, stream, address):
        while True:
            try:
                data = yield stream.read_until(b"\n")
                yield stream.write(data)
            except StreamClosedError:
                break


if __name__ == '__main__':
    server = EchoServer()
    server.listen(8888, '127.0.0.1')
    IOLoop.current().start()
