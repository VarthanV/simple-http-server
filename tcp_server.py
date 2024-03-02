import socket


MAX_LISTENERS = 5
class TCPServer:
    
    def __init__(self,host= '127.0.0.1',port=8888) -> None:
        self.host = host
        self.port = port
        self.max_listeners = MAX_LISTENERS
    
    def start(self):
        s= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.host,self.port))
        s.listen(self.max_listeners)
        print("Listening at ",s.getsockname())
        while True:
            # accept any new connection
            conn, addr = s.accept()
            self.handle_request(conn=conn,addr=addr)
            
          
    def handle_request(self,conn:socket,addr:socket.AddressInfo):
        """
        Handles incoming data and returns a response.
        Override this in subclass.
        """
        pass
  