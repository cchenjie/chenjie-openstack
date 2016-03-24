from webob.dec import wsgify
import webob
import restclient
import json


class Auth(object):
    def __init__(self, app):
        self.app = app

    @classmethod
    def factory(cls, global_config, **local_config):
        def _factory(app):
            return cls(app)
        return _factory

    @wsgify(RequestClass=webob.Request)
    def __call__(self, req):
        resp = self.process_request(req)
        if resp:
            return resp
        return req.get_response(self.app)

    def authenticate_token(self, token, tenant):
        body = "{\"auth\":{\"tenantName\":\"%s\",\"token\":{\"id\":\"%s\"}}}" % (tenant, token)
        resp = restclient.RestClient.post_req(body)
        receive_data = json.loads(resp)
        print json.dumps(receive_data, sort_keys=True, indent=2)
        username = receive_data['access']['user']['username']
        if username is None or username != 'test-swift':
            return webob.exc.HTTPForbidden()

    def process_request(self, req):
        token = req.headers.get('X-Auth-Token')
        tenant = req.headers.get('OS_PROJECT_NAME')
        if token is None or tenant is None:
            return webob.exc.HTTPForbidden()
        else:
            self.authenticate_token(token, tenant)
