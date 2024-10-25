
import json
import socket
from select import select

class Peer:
    
    _table_file: str
    
    def __init__(self, bind, uid: str, address:str, port: int, table_file: str = "./peers.ini") -> None:
        
        self._table_file = table_file
        open(table_file, "a").close()
        data = open(table_file, "r").read()
        if len(data) == 0:
            open(table_file, "w").write(
                "{\"" + uid + "\": {\"address\": \"" + address + "\", \"port\": " + str(port) + "}}"
            )

        self._engine = bind
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(("0.0.0.0", port))
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
        
        conn_type = client_socket.recv(1).decode("utf-8")
        
        if conn_type == "\x01":
            
            peers_data = open(self._table_file, "r").read()
            client_socket.sendall(peers_data.encode("utf-8"))
            
        elif conn_type == "\x02":
        
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

    def hello(self, host: str, post: int) -> None:
        
        peers_data = json.loads(open(self._table_file, "r").read())
        
        try:
            sock = socket.socket()
            sock.connect((host, post))
            sock.sendall("\x01".encode("utf-8"))
            
            data = sock.recv(4096).decode("utf-8")
            if not data:
                return
            
            data_dict = json.loads(data)
            for element in data_dict:
                
                if set(element.keys()) != set(["uid", "address", "port"]):
                    continue
                
                peers_data[element["uid"]] = {
                    "address": element["address"],
                    "port": element["port"]
                }
            
            open(self._table_file, "w").write(
                json.dumps(peers_data)
            )
        except:
            return

    def run(self) -> None:
        
        while not (self.shutdown_flag):
            
            readable, _, _ = select([self.socket], [], [], 1)
            if self.socket in readable:
                client_socket, _ = self.socket.accept()
                self.handle_connection(client_socket)
        
        self.socket.close()
