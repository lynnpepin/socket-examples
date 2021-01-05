"""
test_client.py

Instantiates a SimplestClient, receives 100 pieces of data over it, and repeats the procedure 100 times.

The data is generated deterministically using random.seed, so the client can verify that the server sends the correct data.
"""

from simplest import SimplestClient
import random
import time

if __name__ == "__main__":
    random.seed(413)
    
    total_bytes = 0
    
    start = time.time()
    
    for test_iter in range(100):
        print(f"Client test iteration {test_iter}")
        client = SimplestClient('test.sock', verbose=True)
        #client = SimplestClient(('localhost', 4444), verbose=True)
        for _ in range(100):
            expected_length = random.randint(1,2**18)
            expected_data = bytes([random.randint(0,255) for _ in range(expected_length)])
            data = client.recv()
            assert expected_length == len(data), f"Error, expected {expected_length} bytes, got {len(data)} bytes"
            assert expected_data == expected_data, f"Error: Data mismatch"
            
            total_bytes += expected_length
        
        client.close()
        
    end = time.time()
    
    print(f"Instantiated 100 sockets and sent a total of {total_bytes/1024**2:.2f} MiB in {end-start:.2f} seconds.")
    print(f"... That's about {((total_bytes)/((end-start) * 1024**2)):.2f} MiB/s!")

# Comes out to just under 1 MiB per second... Pretty bad tbh!
# Outer-loop server initialization does not cause significant overhead
