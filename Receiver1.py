from socket import *
import sys


class Receiver:
    def __init__(self):
        self.serverPort = sys.argv[1]
        self.fileName = sys.argv[2]
        self.firstBits = True
        self.EOF = False
        self.clientAddress = None

    def Receive(self, server_socket, data):

        packet, self.clientAddress = server_socket.recvfrom(4000)  # change to 1027?

        # breaking down packet
        sequence_number = packet[0:2]
        eof = packet[2:3]
        imageBytes = packet[3:len(packet)]

        if self.firstBits:
            data = imageBytes
            self.firstBits = False
        else:
            data = data + imageBytes

        if int.from_bytes(eof, 'big') == 1:
            self.EOF = True

        return data, sequence_number

    def BasicFramework(self):
        server_socket = socket(AF_INET, SOCK_DGRAM)
        server_socket.bind(("", int(self.serverPort)))

        print("The server is ready to recieve")

        counter = 0
        data = None
        while not self.EOF:
            data, sequence_number = receiver.Receive(server_socket, data)
        print("HOST RECVD: ", counter, " PACKETS")
        f = open(self.fileName, "w+b")
        f.write(bytearray(data))

        f.close()
        server_socket.close()

if __name__ == "__main__":
    receiver = Receiver()
    receiver.BasicFramework()



