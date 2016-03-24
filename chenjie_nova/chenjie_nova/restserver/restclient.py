import json
import urllib2


class RestClient:
    @classmethod
    def post_req(cls, body, endpoint='https://os-identity.vip.ebayc3.com/v2.0/tokens', method='POST'):
        req = urllib2.Request(endpoint)
        req.get_method = lambda: 'POST'
        req.add_header("content-type", "application/json")
        req.add_data(body)
        resp = urllib2.urlopen(req)
        return resp.read()
