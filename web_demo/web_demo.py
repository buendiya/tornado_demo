
import tornado.ioloop
import tornado.httpclient
from tornado.httpserver import HTTPServer

from tornado.web import RequestHandler, Application, url


class MainHandler(RequestHandler):
    def get(self):
        self.write('<a href="%s">link to story 1</a>' %
                   self.reverse_url("story", "1"))


class StoryHandler(RequestHandler):
    def initialize(self, db):
        self.db = db

    def get(self, *args, **kwargs):
        self.write("this is story %s %s" % (args, kwargs))


class MyFormHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('<html><body><form action="/myform" method="POST">'
                   '<input type="text" name="message">'
                   '<input type="text" name="message">'
                   '<input type="submit" value="Submit">'
                   '</form></body></html>')

    def post(self):
        self.set_header("Content-Type", "text/plain")
        self.write("You wrote " + self.get_body_argument("message") + '\n')
        self.write("You wrote " + ','.join(self.get_body_arguments("message")))


class AsynHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        http = tornado.httpclient.AsyncHTTPClient()
        http.fetch("https://github.com/",
                   callback=self.on_response)

    def on_response(self, response):
        if response.error:
            raise tornado.web.HTTPError(500)
        self.write(response.body)
        self.finish()


class AsynHandler2(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        http = tornado.httpclient.AsyncHTTPClient()
        response = yield http.fetch("https://github.com/")
        self.write(response.body)


def make_app():
    return Application([
        (r"/", MainHandler),
        url(r"/story/([0-9]+)", StoryHandler, dict(db='database'), name="story"),
        url(r"/myform", MyFormHandler),
        url(r"/asyn", AsynHandler),
        url(r"/asyn2", AsynHandler2),
    ])

if __name__ == "__main__":
    app = make_app()
    # app.listen(8888, '127.0.0.1')

    server = HTTPServer(app)
    server.bind(8888, '127.0.0.1')
    server.start(0)

    tornado.ioloop.IOLoop.current().start()
