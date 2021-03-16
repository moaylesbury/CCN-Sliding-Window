from Sender1 import Sender
from socket import *

# extending Sender
class Sender2(Sender):
    def __init__(self):
        super(Sender2, self).__init__()

    def Send2(self):

        # create packets
        # send one packet
        # wait for ack
        # send next packet

        ackReceived = False

        client_socket = socket(AF_INET, SOCK_DGRAM)
        img_byte_arr = Sender.form_image_bytes(self)

        counter = 0
        while img_byte_arr:
            ackReceived = False
            Sender.send(self, client_socket, img_byte_arr[counter], img_byte_arr[counter + 1])

            ackPack, serverAddress = client_socket.recvfrom(4000)
            sequenceNumber = ackPack[0:2]

            if self.sequenceNumber == sequenceNumber:
                ackReceived = True
            else:
                print("error")

            counter += 1


if __name__ == "__main__":
    Sender2()