from socket import *
import sys
import time


class Sender:
    def __init__(self):
        self.remoteHost = sys.argv[1]
        self.serverPort = sys.argv[2]
        self.fileName = sys.argv[3]

    def increment_seq(seq_bytes):
        return (int.from_bytes(seq_bytes, 'big') + 1).to_bytes(2, 'big')


    def Send(self):
        # creating header   /// seq num (two bytes) // EOF (one byte)

        sequenceNumber = (0).to_bytes(2, 'big')
        EOF = (0).to_bytes(1, 'big')

        clientSocket = socket(AF_INET, SOCK_DGRAM)

        # modifiedMessage, serverAddress = clientSocket.recvfrom(bufferSize)

        # working with the image
        bufferSize = 1024
        image = open(self.fileName, "rb")
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

            clientSocket.sendto(packet, (self.remoteHost, int(self.serverPort)))
            time.sleep(0.025)
            counter += 1

            sequenceNumber = self.increment_seq(sequenceNumber)
            imageRead = image.read(bufferSize)
            imageBytes = bytearray(imageRead)

            if len(imageBytes) < bufferSize and len(imageBytes) != 0:
                print("eof! ", counter)
                EOF = (1).to_bytes(1, 'big')

        print("CLIENT SENT: ", counter, " PACKETS")
        clientSocket.close()
        image.close()


if __name__ == "__main__":
    Sender()






