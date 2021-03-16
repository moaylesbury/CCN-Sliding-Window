from socket import *
import sys
import time


class Sender:
    def __init__(self):
        self.remoteHost = sys.argv[1]
        self.serverPort = sys.argv[2]
        self.fileName = sys.argv[3]
        self.sequenceNumber = (0).to_bytes(2, 'big')
        self.EOF = (0).to_bytes(1, 'big')
        self.bufferSize = 1024

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

    def send(self, client_socket, img_byte, img_byte_next):
        # creating header   /// seq num (two bytes) // EOF (one byte)
        # adding header to form image packet

        packet = bytearray(self.sequenceNumber + self.EOF) + img_byte

        # print(int.from_bytes(packet[2:3], 'big'))

        client_socket.sendto(packet, (self.remoteHost, int(self.serverPort)))

        time.sleep(0.025)

        self.sequenceNumber = sender.increment_seq()

        if self.EOF != (1).to_bytes(1, 'big'):
            if len(img_byte_next) < self.bufferSize and len(img_byte_next) != 0:
                print("eof! ")
                self.EOF = (1).to_bytes(1, 'big')

    def BasicFramework(self):
        client_socket = socket(AF_INET, SOCK_DGRAM)
        img_byte_arr = sender.form_image_bytes()

        counter = 0

        while img_byte_arr:
            if self.EOF == (0).to_bytes(1, 'big'):
                sender.send(client_socket, img_byte_arr[counter], img_byte_arr[counter + 1])
            else:
                sender.send(client_socket, img_byte_arr[counter], None)
            counter += 1
        print("CLIENT SENT: ", counter, " PACKETS")
        client_socket.close()


if __name__ == "__main__":
    sender = Sender()
    sender.BasicFramework()