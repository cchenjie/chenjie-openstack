#!/usr/bin/env python
from pkg_resources import load_entry_point


def main():
    print 'Hello World!'
    load_entry_point('chenjie_nova', 'chenjie_nova.cmd.api', 'interface')()
    load_entry_point('chenjie_nova', 'chenjie_nova.cmd.api', 'interface2')()

def interface():
    print 'interface called'

def interface2():
    print 'interface2 called'