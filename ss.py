import random, socket, sys, threading

class ClientThread(threading.Thread):
    def __init__(self, socket):
        threading.Thread.__init__(self)
        self.csock = socket
    def run(self):
        url = self.csock.recv(2048).decode()
        print("Request: %s" % url)
        numSS = self.csock.recv(2048)
        numSS = socket.ntohs(numSS)
        ssChain = []
        ssGotten = 0
        while (ssGotten < numSS):
            ss = self.csock.recv(2048)
            ss = ss.decode()
            ssChain.append(ss)
        

PORT = 54321
HOST = "0.0.0.0"
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

