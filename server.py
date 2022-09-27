from operator import index
import socketserver
from request import RequestProcessor
from response import ResponseHandler

class MyWebServer(socketserver.BaseRequestHandler):
    

    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        request = RequestProcessor(self.data)
        response_handler = ResponseHandler(request)
        self.request.sendall(bytearray(response_handler.handle_response(), 'utf-8'))


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
