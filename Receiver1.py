from socket import *
import sys


serverPort = sys.argv[1]
fileName = sys.argv[2]



serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(("", int(serverPort)))
print("The server is ready to recieve")

firstBits = True
EOF = False

counter = 0

while not EOF:

    packet, clientAddress = serverSocket.recvfrom(4000) # change to 1027

    counter += 1

    sequenceNumber = packet[0:2]
    eof = packet[2:3]
    imageBytes = packet[3:len(packet)]


    if firstBits:
        data = imageBytes
        firstBits = False
    else:
        data = data + imageBytes
    print(int.from_bytes(eof, 'big'), " ", counter)

    if int.from_bytes(eof, 'big') == 1:
        print("END ", counter)
        EOF = True




print("HOST RECVD: ", counter, " PACKETS")
f = open(fileName, "w+b")
f.write(bytearray(data))


f.close()
serverSocket.close()
