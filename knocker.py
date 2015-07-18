#! /usr/bin/env python

import sys
import argparse
import socket
import logging


logger = logging.getLogger('knocker')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(levelname)s] :: %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


class Knocker():

    def __init__(self, host, port_list):
        self.ports = port_list
        self.host = host
        self.msg = ""

    def start_sequence(self):
        transport = 'tcp'
        for port in self.ports:
            if ':' in port:
                splitted = port.split(':')
                port = int(splitted[0])
                transport = splitted[1]
            else:
                port = int(port)
            self.knock(port, transport)

    def knock(self, port, transport_protocol):
        if transport_protocol == 'tcp':
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                sock.connect((self.host, port))
            except Exception, e:
                pass
        elif transport_protocol == 'udp':
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            try:
                sock.sendto(self.msg, (self.host, port))
            except Exception, e:
                logger.warning(e)
        logger.info('Knocking at %s:%d [%s]' % (self.host, port, transport_protocol))


def parse_args(params):
    parser = argparse.ArgumentParser(description='TCP/UDP port knocker')
    parser.add_argument('-t', '--target', help='Targetted host', type=str)
    parser.add_argument('-s', '--sequence', type=str, nargs='+', help='Port sequence. You can specify the protocol for each port')
    return parser.parse_args(params)

if __name__ == '__main__':
    params = parse_args(sys.argv[1:])
    knocker = Knocker(params.target, params.sequence)
    knocker.start_sequence()
