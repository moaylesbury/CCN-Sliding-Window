from socket import *
import sys
import time
import os


class Sender:
    def __init__(self):
        self.remoteHost = sys.argv[1]
        self.serverPort = sys.argv[2]
        self.fileName = sys.argv[3]
        self.sequenceNumber = (0).to_bytes(2, 'big')
        self.EOF = (0).to_bytes(1, 'big')
        self.bufferSize = 1024
        self.fileSize = os.stat(self.fileName).st_size / 1024     # output is in bytes, so divide by 1024 for output in kilobytes

    def increment_seq(self):
        return (int.from_bytes(self.sequenceNumber, 'big') + 1).to_bytes(2, 'big')

    def form_image_bytes(self):
        img_byte_arr = []
        image = open(self.fileName, "rb")
        imageRead = image.read(self.bufferSize)
        imageBytes = bytearray(imageRead)

        img_byte_arr.append(imageBytes)

        while imageBytes:

            imageRead = image.read(self.bufferSize)
            imageBytes = bytearray(imageRead)

            img_byte_arr.append(imageBytes)

        image.close()
        return img_byte_arr

    def send(self, client_socket, img_byte):
        # creating header   /// seq num (two bytes) // EOF (one byte)
        # adding header to form image packet

        if len(img_byte) < self.bufferSize and len(img_byte) != 0:
            print("eof! ")
            self.EOF = (1).to_bytes(1, 'big')

        packet = bytearray(self.sequenceNumber + self.EOF) + img_byte

        # print(int.from_bytes(packet[2:3], 'big'))

        client_socket.sendto(packet, (self.remoteHost, int(self.serverPort)))

        time.sleep(0.025) # TODO: this is important, probably put into one to prevent buffer overload.

        self.sequenceNumber = self.increment_seq()



    def BasicFramework(self):
        client_socket = socket(AF_INET, SOCK_DGRAM)
        img_byte_arr = sender.form_image_bytes()
        # print("LEN: ", len(img_byte_arr))
        counter = 0
        # print("index 879: ", img_byte_arr[878])

        while self.EOF == (0).to_bytes(1, 'big'):
            print(counter)
            sender.send(client_socket, img_byte_arr[counter])
            counter += 1
        print("CLIENT SENT: ", counter, " PACKETS")
        client_socket.close()


if __name__ == "__main__":
    sender = Sender()
    sender.BasicFramework()