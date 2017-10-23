#!/usr/bin/python

import sys
import os
import SimpleHTTPServer
import SocketServer
import BaseHTTPServer
import time

from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


HOST_NAME = "0.0.0.0"
PORT_NUMBER = 80

class QHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        if "favicon" in self.path.lower():
            self.send_response(404, "Not Found")
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write("")
        else:
            res = find_link(self.path)
            if res is None:
                self.send_response(404, "%s is not a known shortcut"%self.path)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write("")
            else:
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.send_header("Location", res)
                self.end_headers()
                self.wfile.write(res)

def not_found(start_response, message="Not Found"):
    start_response("404 Not Found", [])
    return iter([message])

def read(environ, start_response):
    path = environ["PATH_INFO"]
    if "favicon" in path.lower():
        return not_found(start_response)

    res = find_link(path)
    if res is None:
        return not_found(start_response, message="%s is not a known shortcut"%path)
    else:
        start_response("307 Temporary Redirect", [("Content-type", "text/html"), ("Location", res)])
        return iter([res])


def find_link(path):
    with open("shortcuts.yaml") as f:
        last = load(f)
    segments = [seg for seg in path.split('/') if len(seg) > 0]
    for seg in segments:
        if seg in last:
            last = last[seg]
        else:
            return None
    if isinstance(last, dict):
        if '*' in last:
            return last['*']
        else:
            return None
    return last



if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), QHandler)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)
