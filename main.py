import socket
from tcp_server import TCPServer
import logging


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

CRLF = "\r\n\r\n"

class HTTPServer(TCPServer):

    """ 
    raw_data:str Raw data recieved in request
    raw_headers:str Raw headers extracted from the ``raw_data``
    """
    def __init__(self, host='127.0.0.1', port=8888) -> None:
        super().__init__(host, port)
        self.raw_body = ''
        self.raw_headers = ''
        self.raw_data = ''
        self.headers_dict = dict()

    def handle_request(self, conn:socket.SocketType,addr:socket.AddressInfo):
        response_base = 'HTTP/1.0 200 OK Content-Type: text/html {}'.format(CRLF)
        logger.info("Connected by", addr)

        # For debug purpose reading 1024 bytes
        data = conn.recv(1024)
        logging.debug("Data is %s ",data.decode())
        self.raw_data = data.decode()
        try :
         self._parse_request()
        except Exception as e :
            logger.error("Exception in handling  req ",e,exc_info=1)
            conn.sendall(response_base)
            conn.close()
   
        #  Here the request will be parsed and we will have all data
            
        html_file = self._get_html_file()
        response_base += html_file
        conn.sendall(response_base.encode())
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
        logger.debug('Header array is  %s',self.headers_dict)

    def _get_html_file(self):
      try :
        with open('www/{}.html'.format(self.path.split('/')[1]),'r') as f :
            content = f.read()
            return content
      except Exception as e :
        logger.error("Excpetion is %s",exc_info=1,stack_info=True)
        return "<h1> Not found </h1>"

if __name__ == "__main__":
    server = HTTPServer()
    server.start()