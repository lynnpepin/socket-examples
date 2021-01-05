"""
test_server.py

Instantiates a SimplestServer, sends 100 pieces of data over it, and repeats the procedure 100 times.



The data is generated deterministically using random.seed, so the client can verify that the server sends the correct data.
"""

from simplest import SimplestServer
import random

if __name__ == "__main__":
    random.seed(413)
    for test_iter in range(100):
        print(f"Server test iteration {test_iter}")
        server = SimplestServer('test.sock', verbose=True)
        #server = SimplestServer(('localhost', 4444), verbose=True)
        for _ in range(100):
            length = random.randint(1,2**18)
            data = bytes([random.randint(0,255) for _ in range(length)])
            server.send(data)
        
        server.close()

# TODO: Server sometimes hangs, deletes existing socket, causing some kind of race condition...
#       This is an error with the testing procedure. This is a bad way to use the socket!
# 1. One testing iteration finishes
# 2. New client loop starts
# 3. Client connects to existing socket, looks for data
# 4. New server loop starts
# 5. Server sees existing socket, deletes it, waits for connection
#    (But client is still stuck on the old one...)

# Should probably test these over these variables:
# 1. Number of outer iterations
# 2. Number of inner iterations
# 3. Distributions of data length
# 4. Testing with AF_INET address too
# 5. Outer iterations for each (i.e. one big test to reduce the chance this is luck!

# Test runs in about under 30 minutes on my machine, but feel free to end it early!
