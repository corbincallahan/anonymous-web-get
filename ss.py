import random, socket, sys, threading

class ClientThread(threading.Thread):
    def __init__(self, socket):
        threading.Thread.__init__(self)
        self.csock = socket
    def run(self):
        buff = ""
        bytesRecvd = 0
        msgLen = sys.maxsize
        chunk = self.csock.recv(4096).decode()
        if "::" not in chunk:
            print("Error receiving message, exiting")
            sys.exit(1)
        msgLen = int(chunk[:chunk.find("::")])
        buff = chunk[chunk.find("::") + 2:]
        bytesRecvd += len(buff)
        while (bytesRecvd < msgLen):
            chunk = self.csock.recv(min(4096, msgLen - bytesRecvd)).decode()
            buff += chunk
            bytesRecvd += len(chunk)
        print(msgLen, buff)
        
PORT = 54321
HOST = "127.0.0.1"
hostName = socket.gethostname()

if (len(sys.argv) == 3):
    option = sys.argv[1]
    value = sys.argv[2]
    if (option == "-p" and value.isnumeric()):
        PORT = int(value)
    else:
        print("Invalid option specified\nExiting")
        sys.exit(1)

print("ss <%s, %d>:" % (hostName, PORT))

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
lsock.bind((HOST, PORT))
try:
    while True:
        lsock.listen(1)
        csock, cAddr = lsock.accept()
        cThread = ClientThread(csock)
        cThread.start()
except KeyboardInterrupt:
    print("\nCaught keyboard interrupt, exiting")
    sys.exit(0)

