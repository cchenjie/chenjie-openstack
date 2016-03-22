#!/usr/bin/env python
import sys
import chenjie_nova.restserver.service as restserver

server = restserver.WSGIService()


def start_server():
    print "Start the server"
    server.start()
    server.wait()


def stop_server():
    print "Stop the server"
    server.stop()


def restart_server():
    print "Restart the server"
    server.stop()
    server.start()
    server.wait()


def main():
    if len(sys.argv[1:]) != 1:
        error_too_much_args()
        exit(1)

    operator = {'start': start_server,
                'stop': stop_server,
                'restart': restart_server}

    if operator.has_key(sys.argv[1]):
        operator.get(sys.argv[1])()
    else:
        error_invalid_arg()


def error_too_much_args():
    print "Command Error: too much arguments"
    error_format()


def error_invalid_arg():
    print "Command Error: Invalid argument"
    error_format()


def error_format():
    print "Example: chenjie-novaservice start | stop | restart"
