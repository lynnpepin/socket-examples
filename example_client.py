from simplest import SimplestClient

if __name__ == '__main__':
    address = input("Enter chatroom name:")
    client = SimplestClient(address)
    
    while True:
        print(client.recv().decode())
