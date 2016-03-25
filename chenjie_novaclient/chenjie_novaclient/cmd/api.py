#!/usr/bin/env python
import sys
import os
import json
from chenjie_novaclient.restclient.keystoneclient import keystoneclient
from chenjie_novaclient.restclient.novaclient import novaclient

NOVA_EP = "http://127.0.0.1:8080"
TOKEN = ''
TENANT = ''


def index_server():
    global NOVA_EP
    global TOKEN
    global TENANT
    print "List the servers"

    if len(sys.argv[1:]) != 1:
        error_wrong_number_args()
        exit(1)
    resp = novaclient.index(NOVA_EP, TOKEN, TENANT)
    receive_data = json.loads(resp)
    print json.dumps(receive_data, sort_keys=True, indent=2)


def show_server():
    global NOVA_EP
    global TOKEN
    global TENANT
    print "Show a server detail"

    if len(sys.argv[1:]) != 2:
        error_wrong_number_args()
        exit(1)
    server_name = sys.argv[2]
    resp = novaclient.show(NOVA_EP, server_name, TOKEN, TENANT)
    try:
        receive_data = json.loads(resp)
        print json.dumps(receive_data, sort_keys=True, indent=2)
    except Exception, e:
        print resp


def boot_server():
    global NOVA_EP
    global TOKEN
    global TENANT
    print "Boot a server"

    if len(sys.argv[1:]) != 2:
        error_wrong_number_args()
        exit(1)

    server_name = sys.argv[2]
    resp = novaclient.create(NOVA_EP, server_name, TOKEN, TENANT)
    try:
        receive_data = json.loads(resp)
        print json.dumps(receive_data, sort_keys=True, indent=2)
    except Exception, e:
        print resp


def reset_server():
    global NOVA_EP
    global TOKEN
    global TENANT
    print "Update a server"

    if len(sys.argv[1:]) != 3:
        error_wrong_number_args()
        exit(1)

    server_uuid = sys.argv[2]
    server_name = sys.argv[3]
    resp = novaclient.update(NOVA_EP, server_uuid, server_name, TOKEN, TENANT)
    try:
        receive_data = json.loads(resp)
        print json.dumps(receive_data, sort_keys=True, indent=2)
    except Exception, e:
        print resp


def stop_server():
    global NOVA_EP
    global TOKEN
    global TENANT
    print "Stop a server"

    if len(sys.argv[1:]) != 2:
        error_wrong_number_args()
        exit(1)
    resp = novaclient.delete(NOVA_EP, sys.argv[2], TOKEN, TENANT)
    try:
        receive_data = json.loads(resp)
        print json.dumps(receive_data, sort_keys=True, indent=2)
    except:
        print resp


def main():
    global TENANT
    global TOKEN
    if len(sys.argv[1:]) < 1:
        error_invalid_arg()
        exit(1)

    KEYSTONE_EP = check_env('OS_AUTH_URL')
    USER_NAME = check_env('OS_USERNAME')
    PASSWD = check_env('OS_PASSWORD')
    TENANT = check_env('OS_TENANT_NAME')

    TOKEN = keystoneclient.get_auth_token(USER_NAME, PASSWD, TENANT, KEYSTONE_EP)
    if TOKEN is None or TOKEN == '':
        print "Exception: can't get token from Keystone"
        exit(1)
    # print token

    operator = {'list': index_server,
                'show': show_server,
                'boot': boot_server,
                'reset': reset_server,
                'stop': stop_server}

    if operator.has_key(sys.argv[1]):
        operator.get(sys.argv[1])()
    else:
        error_invalid_arg()


def wrong_env_args(env_arg):
    print "Wrong environment arg: %s" % env_arg
    print "Need Environment: OS_AUTH_URL, OS_USERNAME, OS_TENANT_NAME, OS_PASSWORD"


def error_wrong_number_args():
    print "Command Error: wrong number of the arguments"
    error_format()


def error_invalid_arg():
    print "Command Error: Invalid argument"
    error_format()


def error_format():
    print "Example: chenjie-novaclient {list|show|boot|reset|stop}"


def check_env(env_arg):
    if (not os.environ.has_key(env_arg)) or (os.environ[env_arg] == ''):
        wrong_env_args(env_arg)
        exit(1)
    print "%s: %s" % (env_arg, os.environ[env_arg])
    return os.environ[env_arg]