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
    resp = novaclient.show(NOVA_EP, sys.argv[2], TOKEN, TENANT)
    receive_data = json.loads(resp)
    print json.dumps(receive_data, sort_keys=True, indent=2)


def boot_server():
    print "Boot a server"


def reset_server():
    print "Update a server"


def stop_server():
    print "Stop a server"
    global NOVA_EP
    global TOKEN
    global TENANT

    if len(sys.argv[1:]) != 2:
        error_wrong_number_args()
        exit(1)
    resp = novaclient.delete(NOVA_EP, sys.argv[2], TOKEN, TENANT)
    try:
        receive_data = json.loads(resp)
        print json.dumps(receive_data, sort_keys=True, indent=2)
    except:
        receive_data = "The server has been stoped.\n %s" % resp
        print receive_data



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
    if os.environ[env_arg] is None or os.environ[env_arg] == '':
        wrong_env_args(env_arg)
        exit(1)
    print "%s: %s" % (env_arg, os.environ[env_arg])
    return os.environ[env_arg]