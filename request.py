class RequestProcessor:

    def __init__(self, data):
        self.method = None
        self.path = None
        self.__process(data)

    def __process(self, data):

        data_lines = data.split(b"\r\n")
        request_line_values = data_lines[0].split(b" ")
        self.method = request_line_values[0].decode()
        self.path = request_line_values[1].decode()
