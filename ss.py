import random, socket, sys, threading, requests, os

def get_filename(url):
    filename = url.split('/')[-1]
    if "www." in filename:
        filename = "index.html"
    return filename

# From Roman Podlinov at https://stackoverflow.com/questions/16694907/download-large-file-in-python-with-requests/16696317#16696317
def download_file(url):
    local_filename = get_filename(url)
    # NOTE the stream=True parameter below
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                #if chunk: 
                f.write(chunk)
    return local_filename

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
        msgIn = buff.split("\n")
        url = msgIn[0]
        file_name = get_filename(url)
        numSS = int(msgIn[1])
        print("Request: %s" % url)
        if(numSS == 0):
            print("chainlist is empty")
            # GET request using url
            print("issuing wget for file %s" % url.split('/')[-1])
            download_file(url)
            print("File received")
        else:
            # Forward to next SS
            ssChain = msgIn[2:]
            print("chainlist is")
            for ss in ssChain:
                print(ss)
            if (numSS >= 2):
                choice = random.randrange(numSS)
            else:
                choice = 0
            ssAddr = ssChain[choice][1:-1].split(", ")
            ssHost = ssAddr[0]
            ssPort = int(ssAddr[1])
            print("next SS is <%s, %d>" % (ssHost, ssPort))
            numSS -= 1
            ssChain.pop(choice)
            ssSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                ssSock.connect((ssHost, ssPort))
                msg = ""
                msg += url
                msg += "\n" + str(numSS)
                for ss in ssChain:
                    msg += "\n" + ss
                msgLen = len(msg)
                msg = str(msgLen) + "::" + msg
                msg = msg.encode()
                totalSent = 0
                while (totalSent < msgLen):
                    sent = ssSock.send(msg[totalSent:])
                    if sent == 0:
                        raise Exception("")
                    totalSent += sent
            except:
                print("Connection to stepping stone failed, exiting")
                sys.exit(1)
            print("waiting for file...")
            self.recv_file(file_name, ssSock)
            print("file received") 
        print("Relaying file ...")
        self.send_file(file_name)
        # self.remove_file(file_name)

    def recv_file(self, file_name, ssSock):
        # receive file through ssSock
        file_size = int(ssSock.recv(1024).decode())
        amount_read = 0
        with open(file_name, "wb") as f:
            while amount_read < file_size:
                chunk = ssSock.recv(1024)
                if not chunk:
                    break
                f.write(chunk)
                amount_read += len(chunk)

    def send_file(self, file_name):
        # send file through cSock
        file_size = str(os.path.getsize(file_name)).encode()
        self.csock.send(file_size)
        with open(file_name, "rb") as f:
            chunk = f.read(1024)
            while (chunk):
                self.csock.send(chunk)

    def remove_file(self, file_name):
        if os.path.exists(file_name):
            os.remove(file_name)
        else:
            print("File nonexistent and could not be removed, exiting")
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

