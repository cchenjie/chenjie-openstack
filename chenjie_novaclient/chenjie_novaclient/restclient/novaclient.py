__author__ = 'cchenjie'
from chenjie_novaclient.restclient.client import restclient
import json


class novaclient:
    @classmethod
    def index(cls, NOVA_EP, TOKEN, TENANT):
        headers = {}
        headers["X-Auth-Token"] = TOKEN
        headers["OS_PROJECT_NAME"] = TENANT
        return restclient.get_req("%s/instances" % NOVA_EP, headers)

    @classmethod
    def show(cls, NOVA_EP, instanceId, TOKEN, TENANT):
        headers = {}
        headers["X-Auth-Token"] = TOKEN
        headers["OS_PROJECT_NAME"] = TENANT
        return restclient.get_req("%s/instances/%s" % (NOVA_EP, instanceId), headers)

    @classmethod
    def delete(cls, NOVA_EP, instanceId, TOKEN, TENANT):
        headers = {}
        headers["X-Auth-Token"] = TOKEN
        headers["OS_PROJECT_NAME"] = TENANT
        return restclient.delete_req("%s/instances/%s" % (NOVA_EP, instanceId), headers)

    @classmethod
    def create(cls, NOVA_EP, instanceName, TOKEN, TENANT):
        headers = {}
        headers["X-Auth-Token"] = TOKEN
        headers["OS_PROJECT_NAME"] = TENANT
        body = "{\"server\":{\"name\":\"%s\"}}" % instanceName
        return restclient.post_req(body, "%s/instances" % NOVA_EP, headers)

    @classmethod
    def update(cls, NOVA_EP, instanceId, instanceName, TOKEN, TENANT):
        headers = {}
        headers["X-Auth-Token"] = TOKEN
        headers["OS_PROJECT_NAME"] = TENANT
        body = "{\"server\":{\"name\":\"%s\"}}" % instanceName
        return restclient.put_req(body, "%s/instances/%s" % (NOVA_EP, instanceId), headers)
