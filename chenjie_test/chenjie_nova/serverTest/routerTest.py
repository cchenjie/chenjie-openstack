import routes
import routes.middleware
import webob
import webob.dec
from webob.dec import wsgify
import controllers


class Router(object):
    def __init__(self):
        self.mapper = routes.Mapper()
        self.add_routes()
        self._router = routes.middleware.RoutesMiddleware(self._dispatch, self.mapper)

    def add_routes(self):
        controller = controllers.Controller()
        self.mapper.connect("/instances", controller=controller, action="create", conditions=dict(method=["POST"]))
        self.mapper.connect("/instances", controller=controller, action="index", conditions=dict(method=["GET"]))
        self.mapper.connect("/instances/{instance_id}", controller=controller, action="show", conditions=dict(method=["GET"]))
        self.mapper.connect("/instances/{instance_id}", controller=controller, action="update", conditions=dict(method=["PUT"]))
        self.mapper.connect("/instances/{instance_id}", controller=controller, action="delete", conditions=dict(method=["DELETE"]))

    @wsgify(RequestClass=webob.Request)
    def __call__(self, request):
        return self._router

    @staticmethod
    @wsgify(RequestClass=webob.Request)
    def _dispatch(request):
        match = request.environ['wsgiorg.routing_args'][1]
        if not match:
            return _err()

        print "route match result is:", match
        app = match['controller']
        return app


def app_factory(global_config, **local_config):
    return Router()


def _err():
    return {'code': 500, 'message': 'Exception thrown out'}

