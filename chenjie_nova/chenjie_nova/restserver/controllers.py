__author__ = 'cchenjie'
from webob.dec import wsgify
import webob
import uuid
import simplejson


class Controller(object):
    def __init__(self):
        self.instances = {}
        for i in xrange(3):
            inst_id = str(uuid.uuid4())
            self.instances[inst_id] = {'id': inst_id, 'name': 'inst-' + str(i)}

    def create(self, req):
        print(req.params)
        name = req.params['name']
        if name:
            inst_id = str(uuid.uuid4())
            inst = {'id': inst_id, 'name': name}
            self.instances[inst_id] = inst
            return {'id': inst_id, 'instance': inst}

    def index(self, req):
        print(req.params)
        return self.instances

    def show(self, req, instance_id):
        print(req.params)
        return self.instances

    @wsgify(RequestClass=webob.Request)
    def __call__(self, req):
        arg_dict = req.environ['wsgiorg.routing_args'][1]
        action = arg_dict.pop('action')
        del arg_dict['controller']

        method = getattr(self, action)
        result = method(req, **arg_dict)

        if result is None:
            return webob.Response(body='', status='204 Not Found', headerlist=[('Content-Type', 'application/json')])
        else:
            if not isinstance(result, basestring):
                result = simplejson.dumps(result) + '\n'
            return result

