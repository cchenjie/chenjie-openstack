import wsgi


class WSGIService(object):
    def __init__(self):
        self.loader = wsgi.Loader()
        self.app = self.loader.load_app()
        self.server = wsgi.Server(self.app, '127.0.0.1', 8080)

    def start(self):
        self.server.start()

    def wait(self):
        self.server.wait()

    def stop(self):
        self.server.stop()
