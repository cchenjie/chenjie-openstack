import json
import urllib2


class restclient:
    @classmethod
    def post_req(cls, body, endpoint, headers={}):
        return cls.restful_request('POST', endpoint, headers, body)

    @classmethod
    def get_req(cls, endpoint, headers={}):
        return cls.restful_request('GET', endpoint, headers)

    @classmethod
    def delete_req(cls, endpoint, headers={}):
        return cls.restful_request('DELETE', endpoint, headers)

    @classmethod
    def put_req(cls, body, endpoint, headers={}):
        return cls.restful_request('PUT', endpoint, headers, body)

    @classmethod
    def restful_request(cls, method, endpoint, headers, body=""):
        req = urllib2.Request(endpoint)
        req.get_method = lambda: method
        req.add_header("content-type", "application/json")
        for header in headers.keys():
            req.add_header(header, headers[header])

        if method in ("PUT", "POST"):
            req.add_data(body)
        try:
            resp = urllib2.urlopen(req).read()
            return resp
        except Exception, e:
            return e.message


