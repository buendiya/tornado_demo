# encoding: utf-8
"""
先在浏览器里打开：http://127.0.0.1:8888/， 后打开：http://127.0.0.1:8888/normal
可以看到：http://127.0.0.1:8888/normal先打开完成，说明MainHandler是异步的，不影响其他请求

请求：http://127.0.0.1:8888/notasync时，会报错：RuntimeError: Cannot write() after finish()
因为finish已经在RequestHandler的_execute里调用过了

asynchronous装饰器的主要作用是把RequestHandler的_auto_finish置为False，这样在执行到RequestHandler的_execute时，就不会执行如下语句：
    if self._auto_finish and not self._finished:
        self.finish()
finish会在异步的回调里执行
"""

import tornado.ioloop
from tornado import httpclient
from tornado.web import RequestHandler, Application, asynchronous


class MainHandler(RequestHandler):

    @asynchronous
    def get(self):
        http = httpclient.AsyncHTTPClient()
        http.fetch("http://github.com/", self._on_download)

    def _on_download(self, response):
        self.write(response.body)
        self.finish()


class NotAsynchronousHandler(RequestHandler):

    def get(self):
        http = httpclient.AsyncHTTPClient()
        http.fetch("http://github.com/", self._on_download)

    def _on_download(self, response):
        self.write(response.body)
        self.finish()


class NormalHandler(RequestHandler):

    def get(self):
        self.write('Finished')


def make_app():
    return Application([
        (r"/", MainHandler),
        (r"/notasync", NotAsynchronousHandler),
        (r"/normal", NormalHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888, '127.0.0.1')
    tornado.ioloop.IOLoop.current().start()
