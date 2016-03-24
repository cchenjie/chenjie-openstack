import json
import urllib2


class restclient:
    @classmethod
    def post_req(cls, body, endpoint, headers={}):
        req = urllib2.Request(endpoint)
        req.get_method = lambda: 'POST'
        req.add_header("content-type", "application/json")
        for header in headers.keys():
            req.add_header(header, headers[headers])
        req.add_data(body)
        resp = urllib2.urlopen(req)
        return resp.read()

    @classmethod
    def get_req(cls, endpoint, headers={}):
        req = urllib2.Request(endpoint)
        req.get_method = lambda: 'GET'
        req.add_header("content-type", "application/json")
        for header in headers.keys():
            req.add_header(header, headers[header])
        resp = urllib2.urlopen(req)
        return resp.read()

    @classmethod
    def delete_req(cls, endpoint, headers={}):
        req = urllib2.Request(endpoint)
        req.get_method = lambda: 'DELETE'
        req.add_header("content-type", "application/json")
        for header in headers.keys():
            req.add_header(header, headers[header])
        resp = urllib2.urlopen(req)
        return resp.read()
