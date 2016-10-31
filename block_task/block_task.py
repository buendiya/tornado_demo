"""
https://lbolla.info/blog/2013/01/22/blocking-tornado

Try to visit http://localhost:8888/sleep/10 in one tab and http://localhost:8888/ in another:
you'll see that 'Hello, world' is not printed in the second tab until the first one has finished, after 10 seconds.
Effectively, the first call is blocking the IOLoop, who cannot serve the second tab.
"""

import time
import datetime

import tornado.ioloop
import tornado.web


class MainHandler(tornado.web.RequestHandler):

    def get(self):
        self.write("Hello, world %s" % datetime.datetime.now())


class SleepHandler(tornado.web.RequestHandler):

    def get(self, n):
        time.sleep(float(n))
        self.write("Awake! %s" % datetime.datetime.now())


application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/sleep/(\d+)", SleepHandler),
])


if __name__ == "__main__":
    application.listen(8888, '127.0.0.1')
    tornado.ioloop.IOLoop.instance().start()
