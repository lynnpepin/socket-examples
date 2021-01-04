from simplest import SimplestServer

if __name__ == '__main__':
    address = input("Enter chatroom name:")
    server = SimplestServer(address)
    
    while True:
        server.send(input(">>> ").encode('ascii'))
