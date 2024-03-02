import logging
import socket


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

CRLF = "\r\n\r\n"
NEW_LINE=  "\r\n"


class HTTPHandler:
    def __init__(self) -> None:
        self.raw_body = ''
        self.raw_headers = ''
        self.raw_data = ''
        self.headers_dict = dict()
        self.http_method = 'GET'
        self.path = '/'
        self.http_version = '1.1'
        self.conn = None
        self.addr  = None
        self.default_html_file_name = 'index'

    def _get_response_line(self):
        return f'HTTP/1.1 200 OK {NEW_LINE}'
    
    def _get_content_type(self):
        return f'ContentType: text/html; charset=utf-8 {NEW_LINE}'
    
    def handle_request(self, conn:socket.SocketType,addr:socket.AddressInfo):
        response = ''
        self.conn  = conn
        self.addr = addr
        logger.info("Connected by %s", addr)

        # For simplicity reading 1024 bytes
        data = conn.recv(1024)
        logging.debug("Data is %s ",data.decode())
        self.raw_data = data.decode()
        self._parse_request()
        html_file = self._get_html_file()

        response += self._get_response_line()
        response += self._get_content_type()
        response += CRLF
        response += html_file
        conn.send(response.encode())
        conn.close()

    def _parse_request(self):
        _header_data_split = self.raw_data.split(CRLF)
        if len(_header_data_split) == 0:
            raise Exception("Invalid request data")
        
        self.raw_headers =  _header_data_split[0]
        if len(_header_data_split) > 1:
            self.raw_body = _header_data_split[1]

        logger.debug("Raw headers is %s",self.raw_headers)
        logger.debug("Raw body is %s ",self.raw_body)
        self._raw_headers_to_dict()
        
    
    def _raw_headers_to_dict(self):
        splitted_headers = self.raw_headers.split('\n')
        request_line = splitted_headers[0]
        splitted_request_line = request_line.split(' ')

        logger.debug("splitted request line is %s",splitted_request_line)

        # Parse protocol info
        if len(splitted_request_line) != 3  :
           raise Exception("Invalid request line")
        
        self.http_method , self.path, self.http_version = splitted_request_line[0],\
        splitted_request_line[1],splitted_request_line[2]

        logger.debug("HTTP method is %s",self.http_method)
        logger.debug("Path is %s ",self.path)
        logger.debug("HTTP version is %s",self.http_version)
        
        # Parse headers
        if len(splitted_headers) > 1:
            for val in splitted_headers[1:]:
                header_val = val.split(': ')
                if len(header_val) != 2:
                    continue
                key,val =  header_val[0].strip(),header_val[1].strip()
                self.headers_dict[key] = val

        logger.debug("Protocol info is %s",request_line)
        logger.debug('Header dict is  %s',self.headers_dict)

    def _get_html_file(self):
        try :
            file_name  = self.path.split('/')[1]
            if file_name == '':
                file_name = self.default_html_file_name
            with open('www/{}.html'.format(file_name,'r')) as f :
                content = f.read()
                return content
        except FileNotFoundError as e :
            logger.error("Exception is %s",e)
            return "<h1> Not found </h1>"
        
'''
    Response sample

    HTTP/1.1 200 OK
    Content-Type: text/html; charset=utf-8
    Content-Length: 1234

    <!DOCTYPE html>
    <html>
    <head>
        <title>Example Page</title>
    </head>
    <body>
        <h1>Hello, World!</h1>
    </body>
    </html>


'''