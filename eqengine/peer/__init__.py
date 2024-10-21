
import json
import socket
from select import select

class Peer:
    
    def __init__(self, bind, table: str = "./peers.ini") -> None:
        
        self._engine = bind
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(("0.0.0.0", 8080))
        self.socket.listen(5)
        
        self.shutdown_flag = False
    
    def stop(self):
        
        self.shutdown_flag = True

    def handle_request(self, data: list) -> list:

        processed_data = self._engine.request(data)
        return processed_data
    
    def handle_data(self, data: list) -> None:
        
        self._engine.handleData(data)

    def handle_connection(self, client_socket) -> None:
        
        data = client_socket.recv(4096).decode("utf-8")
        
        if not data:
            return
        
        data_dict = json.loads(data)
        if data_dict["type"] == "request":
            response = self.handle_request(data_dict["data"])
            response_json = json.dumps(response)
            client_socket.sendall(response_json.encode("utf-8"))
        elif data_dict["type"] == "data":
            self.handle_data(data_dict["data"])
        
        client_socket.close()

    def run(self) -> None:
        
        while not (self.shutdown_flag):
            
            readable, _, _ = select([self.socket], [], [], 1)
            if self.socket in readable:
                client_socket, _ = self.socket.accept()
                self.handle_connection(client_socket)
        
        self.socket.close()
