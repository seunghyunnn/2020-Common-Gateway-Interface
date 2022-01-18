import sys
import socket
import os
import gzip


# This is the function that parses the configuration file. 
def parse_configuration():
    # Read the configuration file.
    try:
        config_name = sys.argv[1]
        f = open(config_name, 'r')
        config_ls = f.readlines()
        f.close()
    except IndexError:                 
        sys.stderr.write("Missing Configuration Argument\n")
        sys.exit()
    except FileNotFoundError:
        sys.stderr.write("Unable To Load Configuration File\n")
        sys.exit()

    # Retrieve the properties.
    temp = []
    i = 0
    field_check = [False] * 5
    while i<len(config_ls):
        temp = config_ls[i].split("=")
        if temp[0] == "staticfiles":
            staticfiles_p = temp[1].strip()
            field_check[0] = True
        elif temp[0] == "cgibin":
            cgibin_p = temp[1].strip()
            field_check[1] = True
        elif temp[0] == "port":
            port = int(temp[1].strip())
            field_check[2] = True
        elif temp[0] == "exec":
            exec_p = temp[1].strip()
            field_check[3] = True
        else:                          # Wrong field in config file
            field_check[4] = True
        i = i + 1

    # Check whether the configuration file has correct fields.
    i = 0
    contain_four_fields = True
    while i < 4:
        contain_four_fields = contain_four_fields and field_check[i]
        i = i + 1

    if not(contain_four_fields):
        sys.stderr.write("Missing Field From Configuration File\n")
        sys.exit()

    if field_check[4]:
        sys.stderr.write("Wrong Field From Configuration File\n")
        sys.exit()

    return staticfiles_p, cgibin_p, port, exec_p

# This is the function that parses the request. 
def parse_request(request):
    request_data = request.decode().splitlines()
    request_protocol = request_data[0]         # <method> <resouce> <protocol>
    request_data = request_data[1: ]            # <request headers/body>
    
    # Parse the request headers and request body into a dictionary. 
    i = 0
    request_option = {} 
    while i < len(request_data):
        if request_data[i] == "": 
            i = i + 1
            break
        else :
            if ":" in request_data[i]:
                temp = request_data[i].split(": ")
                key = temp[0]
                request_option[key] = temp[1]
            else :
                request_option['body'] += request_data[i] + "\n"
        i = i + 1

    return request_protocol, request_option


# This is the function that checks whether the request 
# is for static_files or for cgi_files. 
def is_this_cgi(request_uri):
    resource = request_uri.split("/")
    if resource[1] == "cgibin":
        return True
    else:
        return False


# This is the function that builds and sends the response 
# related to static files request. 
def handle_static_file_req(staticfiles_p, request_uri, 
                                request_version,  request_option):
    header = request_version
    filepath = staticfiles_p + request_uri.split("?")[0]
    ctype = contenttype(request_uri)
    if request_uri == "/":
        filepath += "index.html"

    if not(os.path.exists(filepath)):
        header += " 404 File not found\n"
        header += "Content-Type: text/html\n\n"
        header = bytes(header, 'utf-8')
        body = ('<html>\n<head>\n\t<title>404 Not Found</title>\n'
    '</head>\n<body bgcolor="white">\n<center>\n\t<h1>404 Not Found</h1>\n'
    '</center>\n</body>\n</html>\n')
        body = bytes(body, 'utf-8')
        return header, body

    else:
        header += " 200 OK\n"
        header += "Content-Type: " + ctype + "\n\n"
        header = bytes(header, 'utf-8')

        # This is the code that builds the gzip body 
        # if the request requires gzipped body.
        if 'Accept-Encoding' in request_option:
            if "gzip" in request_option['Accept-Encoding'].replace(";", " ").\
                                                    replace(",", " ").split():
                header = request_version + " 200 OK\n"
                header += "Content-Type: " + ctype + "\n\n"
                header = bytes(header, 'utf-8')
                f = open(filepath, 'rb')
                content = f.read()
                f.close()
                body = gzip.compress(content)     
                return header, body 

        if ctype == "image/jpeg" or ctype == "image/png":
            f = open(filepath,'rb')
            body = f.read()
            f.close()
            
        else: 
            f = open(filepath, 'r')
            body = f.read()
            f.close()
            body = bytes(body, 'utf-8')

        return header, body


# This is the function that returns the content type 
# of requested file by extension in filename. 
# If there isn't any extension in filename
# it returns "text/html".
def contenttype(request_uri):
    request_uri = request_uri.split("?")[0]         #extract query string
    extension = request_uri.split(".")[-1]

    if extension == "txt":
        return "text/plain"
    elif extension =="html":
        return "text/html"
    elif extension =="js":
        return "application/javascript"
    elif extension =="css":
        return "text/css"
    elif extension =="png":
        return "image/png"
    elif extension =="jpg":
        return "image/jpeg"
    elif extension == "xml":
        return "text/xml"
    elif extension == "/":
        return "text/html"
    else:
        return "text/html"
    

#This function the function that sets the CGI enviornment variables.
def set_cgi_var(server_addr, client_addr, request_method, 
                            request_uri, request_option):
    os.environ['REMOTE_ADDRESS'] = client_addr[0]
    os.environ['REMOTE_PORT'] = str(client_addr[1])
    os.environ['REQUEST_METHOD'] = request_method
    os.environ['REQUEST_URI'] = request_uri.split("?")[0]
    os.environ['SERVER_ADDR'] = server_addr[0]
    os.environ['SERVER_PORT'] = str(server_addr[1])
    if len(request_uri.split("?")) > 1:
        os.environ['QUERY_STRING'] = request_uri.split("?")[1]
    if 'Accept' in request_option:
        os.environ['HTTP_ACCEPT'] = request_option['Accept']
    if 'Host' in request_option:
        os.environ['HTTP_HOST'] = request_option['Host']
    if 'User-Agent' in request_option:
        os.environ['HTTP_USER_AGENT'] = request_option['User-Agent']
    if 'Accept-Encoding'in request_option:
        os.environ['HTTP_ACCEPT_ENCODING'] = request_option['Accept-Encoding']
    if request_method == 'POST':
        if 'Content-Type' in request_option:
            os.environ['CONTENT_TYPE'] = request_option['Content-Type']
        if 'Content-Length' in request_option:
            os.environ['CONTENT_LENGTH'] = request_option['Content-Length']
    

# This is the function that builds and sends the response 
# related to cgi file request. 
def handle_cgi_file_req(cgibin_p, exec_p, request_version, 
                                request_uri, request_option):
    header = request_version
    cgi_uri = request_uri.split("/")[2]
    filename = cgi_uri.split("?")[0]
    filepath = cgibin_p+"/" +filename
    body = ('<html>\n<head>\n\t<title>500 Internal Server Error</title>\n'
    '</head>\n<body bgcolor="white">\n'
    '<center>\n\t<h1>500 Internal Server Error</h1>\n'
    '</center>\n</body>\n</html>\n')

    if not(os.path.exists(filepath)) or not(os.path.exists(exec_p)):
        header += " 500 Internal Server Error\nContent-Type: text/html\n\n"
        header = bytes(header, 'utf-8')
        body = bytes(body, 'utf-8')
        return header, body 

    else :
        wval, result = cgi_execution(exec_p, filename, filepath)

        if wval != 0 :
            header += " 500 Internal Server Error\nContent-Type: text/html\n\n"
            header = bytes(header, 'utf-8')
            body = bytes(body, 'utf-8')
            return header, body

        if len(result) == 0: 
                header += " 200 OK\nContent-Type: text/html\n\n"
                body = result
                header = bytes(header, 'utf-8')
                body = bytes(body, 'utf-8')
                return header, body
        else : 
            if 'Accept-Encoding' in request_option \
        and "gzip" in request_option['Accept-Encoding'].replace(";", " ").\
                                                    replace(","," ").split():
                # This is the code that builds the gzip body
                # if the request requires gzipped body.
                header = request_version + " 200 OK\n"
                header += "Content-Type: text/html" + "\n\n"
                header = bytes(header, 'utf-8')
                i = 0
                body = ""
                while i < len(result):
                    body += result[i]
                    i = i + 1
                body = gzip.compress(bytes(body, 'utf-8'))     
                return header, body

            if "Status-Code" == result[0].split(":")[0]:
                statusline = result.pop(0)
                statuscode = statusline.split(":")[1]
                header += statuscode
            else: 
                header += " 200 OK\n"
               
            if "Content-Type" == result[0].split(":")[0]:
                i = 0
                body = ""
                while i < len(result):
                    body += result[i]
                    i = i + 1
            else: 
                header += "Content-Type: text/html\n\n"
                i = 0
                body = ""
                while i < len(result):
                    body += result[i]
                    i = i + 1

        header = bytes(header, 'utf-8')
        body = bytes(body, 'utf-8')
        return header, body 


# This is the function executes the cgi program
# and returns the exit code and result from executed cgi program. 
def cgi_execution(exec_p, filename, filepath):
    (rfd, wfd) = os.pipe()
    pid = os.fork()
    if pid == 0: 
        os.close(rfd)
        os.dup2(wfd, sys.stdout.fileno())
        os.execve(exec_p, [filename,filepath], os.environ)
        sys.exit()
    elif pid == -1:
        sys.stderr.write("error")
        sys.exit(1)
    else:
        wval = os.wait()
        os.close(wfd)
        r = os.fdopen(rfd,'r')
        result = r.readlines()
        r.close()
    return wval[1]>>8, result


# This is the function that handles a request of individual client
# and send the response back. 
def handle_single_connection(server_socket, client_socket, client_addr,
                                    staticfiles_p, cgibin_p, port, exec_p):
    request = client_socket.recv(1024)
    request_protocol, request_option = parse_request(request)
    request_method = request_protocol.split()[0]
    request_uri = request_protocol.split()[1]
    request_version = request_protocol.split()[2]

    if request_method == "GET":
        if is_this_cgi(request_uri):
            set_cgi_var(server_socket.getsockname(), client_addr,\
                        request_method, request_uri, request_option)
            header, body = handle_cgi_file_req(cgibin_p, exec_p, request_version,\
                                                request_uri, request_option)
        else:
            header, body = handle_static_file_req(staticfiles_p, request_uri,\
                                                 request_version, request_option)
        client_socket.send(header)
        client_socket.send(body)
        client_socket.close()


# This is the function that forks the process 
# for everytime when there is a new connection.
def handle_multi_connection(staticfiles_p, cgibin_p, port, 
                                        exec_p, server_socket):
    while True: 
        client_socket, client_addr = server_socket.accept()
        handle_single_connection(server_socket, client_socket, client_addr, \
                                staticfiles_p, cgibin_p, port, exec_p)


# This is the function that runs first when 
# this script is executed. 
# This function builds the server socket that waits for 
# the connection of clients.
def main():
    staticfiles_p, cgibin_p, port, exec_p = parse_configuration()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    server_socket.bind(('127.0.0.1', port))
    server_socket.listen()
    pid = os.fork()
    if pid == 0:
        handle_multi_connection(staticfiles_p, cgibin_p,port,\
                                exec_p, server_socket)
    handle_multi_connection(staticfiles_p, cgibin_p, port,\
                            exec_p, server_socket)
    server_socket.close()


#This line is initially executed when this program begins.
if __name__=='__main__':
    main()
