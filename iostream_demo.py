# -*- coding: utf-8 -*-

import logging

import tornado.ioloop
import tornado.iostream
import socket


logging.basicConfig()


def write():
    stream.write(b"GET / HTTP/1.0\r\nHost: jd.com\r\n\r\n")


def write_then_stop():
    stream.write(b"GET / HTTP/1.0\r\nHost: jd.com\r\n\r\n", stop)
    import time
    time.sleep(1)
    print 'buffer size: ', stream._read_to_buffer()


def read():
    stream.read_until(b"\r\n\r\n", on_headers)


def send_request():
    write()
    read()


def on_headers(data):
    headers = {}
    for line in data.split(b"\r\n"):
        parts = line.split(b":")
        if len(parts) == 2:
            headers[parts[0].strip()] = parts[1].strip()
    stream.read_bytes(int(headers[b"Content-Length"]), on_body)


def on_body(data):
    print(data)
    stream.close()
    tornado.ioloop.IOLoop.current().stop()


def stop():
    stream.close()
    tornado.ioloop.IOLoop.current().stop()


def start(callback):
    stream.connect(("jd.com", 80), callback)
    tornado.ioloop.IOLoop.current().start()


# default
def test1():
    start(send_request)


# 就算什么也不做，也会触发self.io_loop.WRITE事件
def test2():
    start(stop)


# 写之后立马停止，会触发self.io_loop.READ事件, 且此时read buffer里是有数据的
def test3():
    start(write_then_stop)


if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    stream = tornado.iostream.IOStream(s)
    test1()
