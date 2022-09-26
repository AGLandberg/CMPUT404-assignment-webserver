#https://bhch.github.io/posts/2017/11/writing-an-http-server-from-scratch/
from cgitb import html
import os
import mimetypes
from urllib.request import pathname2url

class ResponseHandler:

    BASE_DIRECTORY = "/www"
    BASE_URL = 'http://127.0.0.1:8080'
    HTTP_VERSION = "HTTP/1.1"
    BLANK_LINE = "\r\n"
    status_code_msg = {
        '200': 'OK',
        '404': 'Not Found',
        '301': 'Moved Permanently',
        '405': 'Method Not Allowed' 
    }

    def __init__(self, request):
        self.request = request
        self.status_code = None
        self.full_path = None
        self.__set_full_path_and_status_code(request.path)

    def handle_response(self):
        return self.__create_status_line() + self.__create_headers_and_body()

    def __set_full_path_and_status_code(self, path):
        #No path needs to be inspected if invalid method is called or insecure path given
        
        if (self.request.method != "GET"):
            self.status_code = "405"
            return
        
        secure_path =self. __check_path_security(path)
        if not secure_path:
            self.status_code = "404"
            return

        self.full_path = os.getcwd() + self.BASE_DIRECTORY + path

        if os.path.exists(self.full_path):
            if os.path.isdir(self.full_path) and self.full_path[-1] != "/":
                self.status_code = "301"
            else:
                self.status_code = "200"
        else:
            self.status_code = "404"
    
    def __create_status_line(self):
        return self.HTTP_VERSION + " " + self.status_code + " " + self.status_code_msg[self.status_code] + self.BLANK_LINE

    def __create_headers_and_body(self):
        if (self.status_code == "200"):
            return self.__handle_200_response()
        elif (self.status_code == "301"):
            return self.__handle_301_response()
        return "\r\n"
                
    def __handle_200_response(self):
        body = None
        if os.path.isdir(self.full_path):
            self.full_path += "index.html"
        with open(self.full_path, "r") as file:
            body = file.read()
        content_type = mimetypes.guess_type(self.full_path)[0]
        content_length = str(len(body.encode('utf-8')))
        return "Content-Type: " + content_type + self.BLANK_LINE + "Content-Length: " + content_length + self.BLANK_LINE*2 + body

    def __handle_301_response(self):
        return "Location: " + self.BASE_URL + self.request.path + "/" + self.BLANK_LINE

    def __check_path_security(self, path):
        if (path.startswith("/..") or "/../../" in path):
            return False
        return True



