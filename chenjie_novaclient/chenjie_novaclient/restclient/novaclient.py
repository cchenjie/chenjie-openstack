__author__ = 'cchenjie'
from chenjie_novaclient.restclient.client import restclient
import json


class novaclient:
    @classmethod
    def get_auth_token(cls, username, passwd, tenant, endpoint='https://os-identity.vip.ebayc3.com/v2.0/tokens'):
        body = '{\"auth\":{\"passwordCredentials\":{\"username\":\"%s\",\"password\":\"%s\"},\"tenantName\": \"%s\"}}'\
               % (username, passwd, tenant)
        resp = restclient.post_req(body, endpoint)
        receive_data = json.loads(resp)
        print json.dumps(receive_data, sort_keys=True, indent=2)
        token = receive_data['access']['token']['id']
        return token

    @classmethod
    def index(cls, NOVA_EP, TOKEN, TENANT):
        headers = {}
        headers["X-Auth-Token"] = TOKEN
        headers["OS_PROJECT_NAME"] = TENANT
        resp = restclient.get_req("%s/instances" % NOVA_EP, headers)
        return resp

    @classmethod
    def show(cls, NOVA_EP, instanceId, TOKEN, TENANT):
        headers = {}
        headers["X-Auth-Token"] = TOKEN
        headers["OS_PROJECT_NAME"] = TENANT
        resp = restclient.get_req("%s/instances/%s" % (NOVA_EP, instanceId), headers)
        return resp

    @classmethod
    def delete(cls, NOVA_EP, instanceId, TOKEN, TENANT):
        headers = {}
        headers["X-Auth-Token"] = TOKEN
        headers["OS_PROJECT_NAME"] = TENANT
        resp = restclient.delete_req("%s/instances/%s" % (NOVA_EP, instanceId), headers)
        return resp
