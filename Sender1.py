from socket import *
import sys
import time

def numToBinary(num, num_bytes):
    return format(num, 'b').zfill(8*num_bytes) # (two bytes = 2*8=16 bits)
def binaryToNum(bin):
    return int(bin, 2)
def increment_seq(seq_bytes):
    return (int.from_bytes(seq_bytes, 'big') + 1).to_bytes(2, 'big')


remoteHost = sys.argv[1]
serverPort = sys.argv[2]
fileName = sys.argv[3]

# creating header   /// seq num (two bytes) // EOF (one byte)

sequenceNumber = (0).to_bytes(2, 'big')
EOF = (0).to_bytes(1, 'big')



clientSocket = socket(AF_INET, SOCK_DGRAM)


# modifiedMessage, serverAddress = clientSocket.recvfrom(bufferSize)

# working with the image
bufferSize = 1024
image = open(fileName, "rb")
imageRead = image.read(bufferSize)
imageBytes = bytearray(imageRead)


counter = 0
while imageBytes:
# while counter < 6:
    # check if EOF


        # print("eof")

    # adding header to image bytes

    packet = bytearray(sequenceNumber + EOF) + imageBytes


    print(int.from_bytes(packet[2:3], 'big'))


    clientSocket.sendto(packet, (remoteHost, int(serverPort)))
    time.sleep(0.025)
    counter += 1

    sequenceNumber = increment_seq(sequenceNumber)
    imageRead = image.read(bufferSize)
    imageBytes = bytearray(imageRead)

    if len(imageBytes) < bufferSize and len(imageBytes) != 0:
        print("eof! ", counter)
        EOF = (1).to_bytes(1, 'big')

print("CLIENT SENT: ", counter, " PACKETS")
clientSocket.close()
image.close()











####
