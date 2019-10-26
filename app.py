import tornado
import tornado.web
import tornado.ioloop
from modules.DownloadManeger import DownloadManeger
import  tornado.template as template
import os
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        # self.write("Lmaooo")
        self.render(r"templates/landing.html")



def make_app():
    settings = dict(
        static_path=os.path.join(os.path.dirname(__file__), "templates", "static")
    )
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/download", DownloadManeger)
        
    ], **settings , debug=True, autoreload=True)



if __name__ == "__main__":
    app = make_app()
    print("Starting server...")
    app.listen(3605)
    print("started on 3605")
    tornado.ioloop.IOLoop.current().start()