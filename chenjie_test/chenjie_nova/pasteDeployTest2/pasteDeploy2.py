from webob import Response
from webob import Request
from webob.dec import wsgify
from paste import httpserver
from paste.deploy import loadapp
import os
import sys

ini_path = os.path.normpath(
    os.path.join(os.path.abspath(sys.argv[0]), os.pardir, 'api-paste.ini')
)

if not os.path.isfile(ini_path):
    print("Cannot find %s\n" % ini_path)
    exit(1)

class Hello(object):
    @wsgify(RequestClass=Request)
    def __call__(self, request):
        return Response('Hello World 2!\n')

def app_factory(global_config, **local_config):
    return Hello()

wsgi_app = loadapp('config:' + ini_path)
httpserver.serve(wsgi_app, host='127.0.0.1', port=8080)