# Tornado: Async Web Framework

from tornado.ioloop import IOLoop
from tornado.web import Application, RequestHandler

class MainHandler(RequestHandler):
    def get(self):
        self.write("Hello, Tornado!")

app = Application([
    (r"/", MainHandler),
])

if __name__ == "__main__":
    app.listen(8888)
    IOLoop.current().start()
