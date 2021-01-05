import socket
import struct
import os


class SimplestServer:
    def __init__(self, address = "simplest.sock", timeout = 60, verbose = True):
        """
        Wraps socket communication for a simple simplex protocol. The server
        is used to send data to a client, and receives nothing back.
        
        Address type is inferred as AF_INET or AF_UNIX.
        
        :param address: Tuple of string and int (for AF_INET), or string (for AF_UNIX).
        :param timeout: Float. Maximum waiting time (in seconds) for blocking actions.
        :param verbose: If True, print extra debug info.
        :method send: Sends data to the given address through the initialized socket.
    
        usage:
        server = SimplestServer(address=('localhost', 6000))
        # or server = SimplestServer(address='somewhere.sock')
        server.send(b'here_is_some_data!')
        server.send(b'and some more data')
        for x in range(100):
            server.send(struct.pack('<q', x**x))
        """
        
        self.V = verbose
        self.address = address
        
        # 1. Infer socket address family as either AF_INET or AF_UNIX
        if type(self.address[0]) is str and type(self.address[1]) is int:
            if self.V: print("Setting address family as AF_INET")
            self.AF = socket.AF_INET
        elif type(self.address) is str:
            self.AF = socket.AF_UNIX
        else:
            raise ValueError("Addresses must be formatted for either AF_INET or AF_UNIX.")
        
        # 2. If using AF_INET, check for existing socket before creating
        if self.AF == socket.AF_INET:
            pass
            # TODO: Check for existing IPv4 socket here!
        # 2. If using AF_UNIX, check for existing socket before creating
        elif self.AF == socket.AF_UNIX:
            if self.V: print("Checking for existing socket...")
            if os.path.exists(self.address):
                if self.V: print("... It exists! Destructing existing socket...")
                os.remove(self.address)
            elif self.V: print("... No socket found!")

        # 3. Instantiate socket
        if self.V: print("Creating socket...")
        self.serversocket = socket.socket(self.AF, socket.SOCK_STREAM)
        self.serversocket.settimeout(timeout)
        
        if self.V: print(f"... binding to {self.address} ...")
        self.serversocket.bind(self.address)
        
        if self.V: print("... Bound! Listening...")
        self.serversocket.listen()
        
        if self.V: print("... Found connection! Accepting...")
        self.clientsocket, self.clientaddr = self.serversocket.accept()
        
        if self.V: print(f"... Accepted, Connected to client at addr {self.clientaddr}")
    
    def close(self):
        self.serversocket.close()
        self.clientsocket.close()
    
    def __del__(self):
        self.close()
        
    def send(self, data, verbose = None):
        """Send data over the instantiated socket.
        
        :param data: Raw data of length
        :param verbose: Bool
            If True, print debug data
            If False, do not print debug data
            If None, infer from 'verbose' set during initialization
        """
        # set verbosity
        VV = self.V if verbose is None else verbose
        
        # send length of data
        if VV: print(f"Sending length of data {len(data)} ...")
        num_bytes = struct.pack('<q', len(data))
        self.clientsocket.send(num_bytes)
        if VV: print(f"... Sent!")
        
        # send data
        if VV: print(f"... Sending actual data ...")
        self.clientsocket.send(data)
        if VV: print(f"... Sent!")

# TODO from here down
class SimplestClient:
    def __init__(self, address = "simplest.sock", timeout = 60,  verbose = True):
        """
        Wraps socket communication for a simple simplex protocol. The client
        is used to receive data from a server, and sends nothing back.
        
        Address type is inferred as AF_INET or AF_UNIX.
        
        :param address: Tuple of string and int (for AF_INET), or string (for AF_UNIX).
        :param timeout: Float. Maximum waiting time (in seconds) for blocking actions.
        :param verbose: If True, print extra debug info.
        :method recv: Returns data received from the initialized socket.
         
        usage: 
        client = SimplestClient(address=('localhost', 6000))
        # or this: client = SimplestClient(address='somewhere.sock')
        while True:
            data = client.recv()
            ...
        """
        self.V = verbose
        self.address = address
        
        
        # 1. Infer socket address family as either AF_INET or AF_UNIX
        if type(self.address[0]) is str and type(self.address[1]) is int:
            if self.V: print("Setting address family as AF_INET")
            self.AF = socket.AF_INET
        elif type(self.address) is str:
            self.AF = socket.AF_UNIX
        else:
            raise ValueError("Addresses must be formatted for either AF_INET or AF_UNIX.")
        
        # 2. Instantiate socket
        if self.V: print(f"Creating socket...")
        self.socket = socket.socket(family=self.AF, type=socket.SOCK_STREAM)
        self.socket.settimeout(timeout)
        
        # 3. Connect to socket
        if self.V: print(f"... connecting to socket at {self.address}...")
        connected = False
        while not connected:
            try:
                self.socket.connect(self.address)
                connected = True
            except Exception as e:
                pass
        if self.V: print(f"... Done!")
        
        # 4. Buffering data
        # Necessary for larger data packets
        self.buffer = b''

    def close(self):
        self.socket.close()
    
    def __del__(self):
        self.close()
    
    def recv(self, verbose = None):
        """
        Receive and return raw data.
        
        :param verbose: Bool
            If True, print debug data
            If False, do not print debug data
            If None, infer from 'verbose' set during initialization
        """
        # set verbosity
        VV = self.V if verbose is None else verbose
        
        # reset buffer
        self.buffer = b''
        
        # receive length of data
        if VV: print("Receiving length of data...")
        num_bytes = self.socket.recv(8)
        num_bytes = struct.unpack('<q', num_bytes)[0]
        if VV: print(f"... Received length {num_bytes} ...")
        
        # receive data
        if VV: print(f"... Receiving bytes ...")
        # nheads up, there are probably more efficient ways to work with a buffer
        while len(self.buffer) < num_bytes:
            bytes_to_read = num_bytes - len(self.buffer)
            self.buffer += self.socket.recv(bytes_to_read)
            
        if VV: print(f"... Received all bytes!")
        
        return self.buffer
        
