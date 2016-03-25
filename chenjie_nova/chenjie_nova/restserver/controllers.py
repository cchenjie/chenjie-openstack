__author__ = 'cchenjie'
from webob.dec import wsgify
import webob
import uuid
import simplejson as json


class Controller(object):
    def __init__(self):
        self.instances = {}
        for i in xrange(3):
            inst_id = str(uuid.uuid4())
            self.instances[inst_id] = {'id': inst_id, 'name': 'inst-' + str(i)}

    def create(self, req):
        request = json.loads(req.body)
        name = request['server']['name']
        if name is not None and name != "":
            inst_id = str(uuid.uuid4())
            inst = {'id': inst_id, 'name': name}
            self.instances[inst_id] = inst
            return {'id': inst_id, 'instance': inst}

    def index(self, req):
        return {'instances': self.instances.values()}

    def show(self, req, instance_id):
        inst = self.instances.get(instance_id)
        return {'instance': inst}

    def update(self, req, instance_id):
        inst = self.instances.get(instance_id)
        request = json.loads(req.body)
        name = request['server']['name']

        if (name is not None and name != "") and (inst is not None and inst != ""):
            inst['name'] = name
            return {'instance': inst}
        else:
            return Exception("404 Instance Not Found")

    def delete(self, req, instance_id):
        if self.instances.get(instance_id):
            self.instances.pop(instance_id)
            return "The server %s has been stoped" % instance_id

    @wsgify(RequestClass=webob.Request)
    def __call__(self, req):
        arg_dict = req.environ['wsgiorg.routing_args'][1]
        action = arg_dict.pop('action')
        del arg_dict['controller']

        method = getattr(self, action)
        result = method(req, **arg_dict)

        if result is None:
            return webob.Response(body='', status='204 Not Found', headerlist=[('Content-Type', 'application/json')])
        if isinstance(result, Exception):
            print(result)
            return webob.Response(body=result.message, status=result.message, headerlist=[('Content-Type', 'application/json')])
        else:
            if not isinstance(result, basestring):
                result = json.dumps(result) + '\n'
            return result

