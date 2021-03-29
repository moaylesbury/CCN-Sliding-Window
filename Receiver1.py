# Michael Aylesbury s1751472

from socket import *
import sys


class Receiver:
    def __init__(self):
        self.serverPort = sys.argv[1]       # port number from input
        self.fileName = sys.argv[2]         # file name to create and write to  from input
        self.firstBits = True               # initialise first bits received to True
        self.EOF = False                    # intiialise end of file flag to False
        self.clientAddress = None           # initialise client address to None

    def Receive(self, server_socket):

        # receive packet and client address from socket
        packet, self.clientAddress = server_socket.recvfrom(8000)
        # parse packet
        sequence_number = packet[0:2]
        eof = packet[2:3]
        image_bytes = packet[3:len(packet)]

        # if end of file from bytes is equal to 1 set EOF to True
        if int.from_bytes(eof, 'big') == 1:
            self.EOF = True

        # return data and sequence number
        return image_bytes, sequence_number

    def append_data(self, data, image_bytes):
        # if data is None then set data to image bytes
        if data is None:
            data = image_bytes
        # otherwise append image bytes to data
        else:
            data = data + image_bytes
        # return data
        return data

    def WriteDataCloseSocket(self, data, socket):
        # open file to write bytes
        f = open(self.fileName, "w+b")
        # write bytearray of data to file
        f.write(bytearray(data))

        # close file
        f.close()
        # close socket
        socket.close()

    def BasicFramework(self):
        # create UDP server socket
        server_socket = socket(AF_INET, SOCK_DGRAM)
        # bind socket to server port
        server_socket.bind(("", int(self.serverPort)))

        # initialise counter to 0
        counter = 0
        # initialise data to None
        data = None

        # while not received end of file flag
        while not self.EOF:
            # receive image bytes and sequence number from socket
            image_bytes, sequence_number = receiver.Receive(server_socket)
            # append image bytes to data
            receiver.append_data(data, image_bytes)

        receiver.WriteDataCloseSocket(data, server_socket)




if __name__ == "__main__":
    receiver = Receiver()
    receiver.BasicFramework()
