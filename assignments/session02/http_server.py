import socket
import sys
import os
from urlparse import urlparse
import urllib, mimetypes

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
    #home = (sys.path[0] + '/webroot')
    #uri = '/sample.txt'
    #uri = '/a_web_page.html'
    #uri = '/\images/sample_1.png'
    #uri = '/images/JPEG_example.jpg'
    #uri = '/missing.html'
    if uri == '/\images/sample_1.png':
        uri = '/images/sample_1.png'
    url = (sys.path[0] + '/webroot' + uri)
    dir_list = []
    # if uri exists as path...
    # import pdb; pdb.set_trace()
    if os.path.isdir(url):
        # ...create a list with the contents
        uri_dir = os.listdir(url)
        # convert unicode list to printable list
        for word in (uri_dir):
            dir_list.append(str(word))
        return dir_list, 'text/plain'
    elif os.path.isfile(url):
        uni_url = urllib.pathname2url(url)
        #url = '/images/sample_1.png'
        try:
            obj_file = open(url, 'rb')
            file_content = obj_file.read()
            obj_file.close()
            return file_content, mimetypes.guess_type(uni_url)[0]
        except:
            return response_not_found()
            raise ValueError
##        except IOError:
##            raise Exception ("Error reading: can\'t access file.")
            #return response_not_found()
    else:
        #import pdb; pdb.set_trace()
        #raise ValueError
        try:
            return response_not_found(), ''
        except ValueError:
            pass

##        except IOError:
##            raise Exception ("Error reading: can\'t access file.")
        #except:
        #    raise Exception ("Error: some problem happened while reading file; not sure what.")
        #print repr(file_content)

        #import pdb; pdb.set_trace()
        return file_content, mimetypes.guess_type(uni_url)[0]
##    else:
##        return response_not_found()
##        raise Exception ('404 Not Found')


def response_not_found():
    return 'HTTP/1.1 404 Not Found'
    raise ValueError



def response_ok(body, mimetype):
    """returns a basic HTTP response"""
    resp = []
    resp.append("HTTP/1.1 200 OK")
    if mimetype == 'image/pjpeg':
        resp.append('image/jpeg\r\n')
    elif mimetype == "":
        resp.append("Content-Type: text/plain")
        #resp.append("Content-Type: text/plain or No mimetype found")
    elif mimetype != "":
        resp.append("Content-Type: " + mimetype + '\r\n')
    if body != "" and body:
        resp.append(body)
    else:
        resp.append("this is a pretty minimal response")
    #resp.append(mimetype)
    #resp.append("")
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
                    uri = parse_request(request)
                except NotImplementedError:
                    response = response_method_not_allowed()
                    #raise NotImplementedError (response)
                    print (response)
                else:
                    try:
                        #import pdb; pdb.set_trace()
                        #if content != '' and mimetype != '':
                        content, mimetype = resolve_uri(uri)
                    except ValueError:
                        #raise ValueError('404 Not Found')
                        print ('404 Not Found')
                    #response = response_ok()
                    if content != '':
                        if content != 'HTTP/1.1 404 Not Found':
                            response = response_ok(str(content), str(mimetype))
                        else:
                            response = str(content) + ',' + str(mimetype) + '\r\n\r\n404 ' + uri + ' not found.'
                            #raise ValueError
                    else:
                        response = str(content) + ',' + str(mimetype)

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
