import socket
from tcp_server import TCPServer
from http_handler import HTTPHandler
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

    def handle_request(self, conn:socket.SocketType,addr:socket.AddressInfo):
        try :
            http_handler = HTTPHandler()
            http_handler.handle_request(conn=conn,addr=addr)
        except Exception as e :
            logger.error("Exception in handling  req %s ",e,exc_info=1)
            conn.close()
     
if __name__ == "__main__":
    server = HTTPServer()
    server.start()