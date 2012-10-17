import BaseHTTPServer
import gflags
import os
import sys

FLAGS = gflags.FLAGS

gflags.DEFINE_integer('delay', 60, 'Number of seconds between updates on the live server')
gflags.DEFINE_integer('port', 2012, 'Port to listen on')
gflags.DEFINE_string('host', '127.0.0.1', 'Host to bind to')
gflags.DEFINE_string('docroot', os.chdir(), 'Document root')


class HandlerClass(BaseHTTPServer):
    pass

ServerClass  = BaseHTTPServer.HTTPServer
Protocol     = "HTTP/1.0"

def main(argv):
    try:
        argv = FLAGS(argv)[1:]
    except gflags.FlagsError, e:
        print "Usage: %s ARGS\\n%s" % (sys.argv[0], FLAGS)
        return 1
    
    server_address = (GFLAGS.host, GFLAGS.port)
    sa = httpd.socket.getsockname()
    log.INFO("Serving HTTP on %s port %s " % tuple(sa))
    
    HandlerClass.protocol_version = Protocol
    httpd = ServerClass(server_address, HandlerClass)

    httpd.serve_forever()

    
