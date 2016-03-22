from webob.dec import wsgify
from paste import httpserver
from paste.deploy import loadapp
import webob
import controllers
import os
import sys
import routes
import routes.middleware

ini_path = os.path.normpath(
    os.path.join(os.path.abspath(sys.argv[0]), os.pardir, 'api-paste.ini')
)

if not os.path.isfile(ini_path):
    print("Cannot find %s\n" % ini_path)
    exit(1)


class Router(object):
    def __init__(self):
        self.mapper = routes.Mapper()
        self.add_routes()
        self._router = routes.middleware.RoutesMiddleware(self._dispatch, self.mapper)

    def add_routes(self):
        controller = controllers.Controller()
        self.mapper.connect("/instances", controller=controller, action="get_all", conditions=dict(method=["GET"]))
        self.mapper.connect("/instances/{id}", controller=controller, action="get", conditions=dict(method=["GET"]))
        self.mapper.connect("/instances", controller=controller, action="create", conditions=dict(method=["POST"]))

    @wsgify(RequestClass=webob.Request)
    def __call__(self, request):
        return self._router

    @staticmethod
    @wsgify(RequestClass=webob.Request)
    def _dispatch(request):
        match = request.environ['wsgiorg.routing_args'][1]
        if not match:
            return _err()
        app = match['controller']
        return app


def app_factory(global_config, **local_config):
    return Router()

wsgi_app = loadapp('config:' + ini_path)
httpserver.serve(wsgi_app, host='127.0.0.1', port=8080)
