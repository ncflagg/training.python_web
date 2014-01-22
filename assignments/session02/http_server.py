import socket
import sys
import os
from urlparse import urlparse
'''
    url = 'http://example.com/random/folder/path.html'
    parse_object = urlparse(url)
    parse_object.netloc
    # 'example.com'
    parse_object.path
    # '/random/folder/path.html'
'''

def resolve_uri(uri):
    # get home dir (start with script location)
    home = (sys.path[0])
    dir_list = []
    # if uri exists as path...
    if os.path.isdir(home + '/webroot' + uri):
        # ...create a list with the contents
        uri_dir = os.listdir(home + '/webroot' + uri)
        # convert unicode list to printable list
        for x, word in enumerate(uri_dir):
            dir_list.append(str(word))
        return dir_list, 'text/plain'






def response_ok(body, mimetype):
    """returns a basic HTTP response"""
    resp = []
    resp.append("HTTP/1.1 200 OK")
    if mimetype != "":
        resp.append("Content-Type: text/plain")
    else:
        resp.append(mimetype)
    resp.append("")
    if body != "":
        resp.append(body)
    else:
        resp.append("this is a pretty minimal response")
    return "\r\n".join(resp)


def response_method_not_allowed():
    """returns a 405 Method Not Allowed response"""
    resp = []
    resp.append("HTTP/1.1 405 Method Not Allowed")
    resp.append("")
    return "\r\n".join(resp)


def parse_request(request):
    first_line = request.split("\r\n", 1)[0]
    method, uri, protocol = first_line.split()
    if method != "GET":
        raise NotImplementedError("We only accept GET")
    print >> sys.stderr, 'request is okay'
    # return first_line [everything after 'Get /' up to next space]
    return uri


def server():
    address = ('127.0.0.1', 10000)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print >>sys.stderr, "making a server on %s:%s" % address
    sock.bind(address)
    sock.listen(1)

    try:
        while True:
            print >>sys.stderr, 'waiting for a connection'
            conn, addr = sock.accept() # blocking
            try:
                print >>sys.stderr, 'connection - %s:%s' % addr
                request = ""
                while True:
                    data = conn.recv(1024)
                    request += data
                    if len(data) < 1024 or not data:
                        break

                try:
                    parse_request(request)
                except NotImplementedError:
                    response = response_method_not_allowed()
                else:
                    response = response_ok()

                print >>sys.stderr, 'sending response'
                conn.sendall(response)
            finally:
                conn.close()

    except KeyboardInterrupt:
        sock.close()
        return




if __name__ == '__main__':
    server()
    sys.exit(0)
