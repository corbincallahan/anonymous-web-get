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
        
        msgIn = buff.split("\n")
        url = msgIn[0]
        numSS = int(msgIn[1])
        if(numSS == 0):
            # GET request using url
            print("Getting from url")
        else:
            # Forward to next SS
            ssChain = msgIn[2:]
            
            if (numSS >= 2):
                choice = random.randrange(numSS)
            else:
                choice = 0
            ssAddr = ssChain[choice][1:-1].split(", ")
            ssHost = ssAddr[0][1:-1]
            ssPort = int(ssAddr[1])
            numSS -= 1
            ssChain.pop(choice)
            ssSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                ssSock.connect((ssHost, ssPort))
                msg = ""
                msg += url
                msg += "\n" + str(numSS)
                for ss in ssChain:
                    msg += "\n" + str(ss)
                msgLen = len(msg)
                msg = str(msgLen) + "::" + msg
                msg = msg.encode()
                totalSent = 0
                while (totalSent < msgLen):
                    sent = ssSock.send(msg[totalSent:])
                    if sent == 0:
                        raise Exception("")
                    totalSent += sent
            except OSError:
                print("Connection to stepping stone failed, exiting")
                sys.exit(1)
        
        
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

