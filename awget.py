import socket, sys, random

fileName = "chaingang.txt"
url = sys.argv[1]
ssChain = []
numSS = 0

if (len(sys.argv) == 4):
    option = sys.argv[2]
    value = sys.argv[3]
    if (option == "-c"):
        fileName = value
    else:
        print("Invalid chainfile name, exiting")
        sys.exit(1)
elif (len(sys.argv) != 2):
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
print("Chainlist is")
for ss in ssChain:
    print("<%s, %s>" % (ss[0], ss[1]))

if (numSS >= 2):
    choice = random.randrange(numSS - 1)
else:
    choice = 0
ssAddr = ssChain[choice]
ssSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print(ssAddr)
try:
    ssSock.connect(ssAddr)
    numSS -= 1
    ssChain.pop(choice)
    msg = ""
    msg += url
    msg += str(numSS)
    msg += str(ssChain)
    msgLen = len(msg)
    msg = str(msgLen) + "::" + msg
    print(msg)
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


# print("Received file %s" % outFileName)

