# Michael Aylesbury s1751472

from socket import *
import sys
import time
import os


class Sender:
    def __init__(self):
        # initialising self variables
        self.remoteHost = sys.argv[1]                           # address for socket from input
        self.serverPort = sys.argv[2]                           # port number for socket from input
        self.fileName = sys.argv[3]                             # name of file to be transferred from input
        self.sequenceNumber = (0).to_bytes(2, 'big')            # sequence number for transferred packet, initialised as 0
        self.EOF = (0).to_bytes(1, 'big')                       # end of file flag, 0 if not EOF, 1 otherwise
        self.bufferSize = 1024                                  # buffer size
        self.fileSize = os.stat(self.fileName).st_size / 1024   # size of input file. output is in bytes, so divide by 1024 for output in kilobytes

    def increment_seq(self):
        # Input: self
        # Output: sequence number + 1 in bytes
        return (int.from_bytes(self.sequenceNumber, 'big') + 1).to_bytes(2, 'big')

    def form_image_bytes(self):
        # Input: self
        # Output: array of bytearrays read from file, each bytearray of size self.bufferSize
        img_byte_arr = []
        # open file
        image = open(self.fileName, "rb")
        # read self.bufferSize bytes
        imageRead = image.read(self.bufferSize)
        # convert read bytes to bytearray
        imageBytes = bytearray(imageRead)
        # add bytearray to img_byte_arr
        img_byte_arr.append(imageBytes)

        # read self.bufferSize bytes, make bytearray, append to img_byte_arr until no more bytes can be read
        while imageBytes:

            imageRead = image.read(self.bufferSize)
            imageBytes = bytearray(imageRead)

            img_byte_arr.append(imageBytes)

        # close file
        image.close()
        # return array
        return img_byte_arr

    def send(self, client_socket, img_byte):
        # Input:  self, client_socket, img_byte
        # Output: N/A

        # if the img_byte is smaller than the buffer size and non-zero, then it must be the final byte
        if len(img_byte) < self.bufferSize and len(img_byte) != 0:
            # set the EOF flag to 1 to indicate end of file
            self.EOF = (1).to_bytes(1, 'big')

        # create packet by adding sequence number and end of file header to the img_byte
        packet = bytearray(self.sequenceNumber + self.EOF) + img_byte

        # send the packet using the client socket
        client_socket.sendto(packet, (self.remoteHost, int(self.serverPort)))

        # briefly sleep to prevent buffer overflow on receiver end
        time.sleep(0.025)

        # increment sequence number
        self.sequenceNumber = self.increment_seq()

    def BasicFramework(self):
        # Input:  self
        # Output: N/A

        # create UDP client socket
        client_socket = socket(AF_INET, SOCK_DGRAM)
        # form image bytes
        img_byte_arr = sender.form_image_bytes()
        # initialise counter to 0
        counter = 0
        # start timer
        begin_time = time.time()

        # loop until end of file
        while self.EOF == (0).to_bytes(1, 'big'):
            # send counterth img_byte over client_socket
            sender.send(client_socket, img_byte_arr[counter])
            # increment counter
            counter += 1
        # close client socket
        client_socket.close()
        # print throughput
        time_elapsed = time.time() - begin_time
        print(self.fileSize / time_elapsed)


if __name__ == "__main__":
    sender = Sender()
    sender.BasicFramework()
