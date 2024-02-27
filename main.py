import socket
from tcp_server import TCPServer
import logging


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

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
        response = 'HTTP/1.0 200 OK\n\nHello World'
        print("Connected by", addr)

        data = conn.recv(1024)
        logging.debug("Data is %s ",data.decode())
        self.raw_data = data.decode()
        try :
         self._parse_request()
        except Exception as e :
            logger.error("Exception in handling  req ",e,exc_info=1)
            conn.sendall(response)
            conn.close()
   
        conn.sendall(response.encode())
        conn.close()

    def _parse_request(self):
        _header_data_split = self.raw_data.split('\n\n')
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
        protocol_info = splitted_headers[0]
        splitted_protocol_info = protocol_info.split(' ')

        print("splitted info is ",splitted_protocol_info)

        # Parse protocol info
        if len(splitted_protocol_info) != 3  :
           raise Exception("Invalid protocol info")
        
        http_method , path, http_version = splitted_protocol_info[0],\
        splitted_protocol_info[1],splitted_protocol_info[2]
        logger.debug("HTTP method is %s",http_method)
        logger.debug("Path is %s ",path)
        logger.debug("HTTP version is %s",http_version)
        
        # Parse headers
        if len(splitted_headers) > 1:
    

            for val in splitted_headers[1:]:
                header_val = val.split(': ')
                if len(header_val) != 2:
                    continue
                key,val =  header_val[0].strip(),header_val[1].strip()
                self.headers_dict[key] = val

        logger.debug("Protocol info is %s",protocol_info)
        logger.debug('Header array is  %s',self.headers_dict)



if __name__ == "__main__":
    server = HTTPServer()
    server.start()