import socket, sys, random, os
from urllib.parse import urlparse

fileName = "chaingang.txt"
url = ""
ssChain = []
numSS = 0

if (len(sys.argv) == 2):
    url = sys.argv[1]
elif (len(sys.argv) == 4):
    if (sys.argv[1] == "-c"):
        fileName = sys.argv[2]
        url = sys.argv[3]
    elif (sys.argv[2] == "-c"):
        fileName = sys.argv[3]
        url = sys.argv[1]
    else:
        print("Invalid arguments, exiting")
        sys.exit(1)
else:
    print("Invalid arguments, exiting")
    sys.exit(1)

try:
    with open(fileName, "r") as chainfile:
        numSS = int(chainfile.readline())
        for line in chainfile:
            if (line == "" or line == "\n"):
                break
            info = line.split()
            if (len(info) != 2):
                raise Exception("")
            ssAddr = info[0]
            ssPort = int(info[1])
            ssChain.append((ssAddr, ssPort))
except:
    print("Unable to read in chainfile, exiting")
    sys.exit(1)

print("Request: %s" % url)
print("chainlist is")
for ss in ssChain:
    print("<%s, %s>" % (ss[0], ss[1]))

if (numSS >= 2):
    choice = random.randrange(numSS)
else:
    choice = 0
ssAddr = ssChain[choice]
ssSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("next SS is <%s, %s>" % (ssAddr[0], ssAddr[1]))
try:
    ssSock.connect(ssAddr)
    numSS -= 1
    ssChain.pop(choice)
    msg = ""
    msg += url
    msg += "\n" + str(numSS)
    for ss in ssChain:
        msg += "\n" + ("<%s, %s>" % (ss[0], ss[1]))
    msgLen = len(msg)
    msg = str(msgLen) + "::" + msg
    #print(msg)
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

print("Waiting for file...")
a = urlparse(url)
file_name = os.path.basename(a.path)
if file_name == '':
    file_name = "index.html"
file_size = int(ssSock.recv(1024).decode())
amount_read = 0
f = open(file_name, "wb")
while amount_read < file_size:
    chunk = ssSock.recv(1024)
    if not chunk:
        break
    f.write(chunk)
    amount_read += len(chunk)
    

print("Received file %s" % file_name)

