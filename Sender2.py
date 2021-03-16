from Sender1 import Sender
from socket import *
import time

# extending Sender
class Sender2(Sender):
    def __init__(self):
        super(Sender2, self).__init__()

    def SendAndWait(self, img_byte_arr, client_socket, counter):
        # create packets
        # send one packet
        # wait for ack
        # send next packet

        ack_received = False
        time_elapsed = 0
        timeout_time = 0  # rtt multiple

        while self.EOF == (0).to_bytes(1, 'big'):

            # send packet
            sender2.Sender.send(client_socket, img_byte_arr[counter])
            # start timer
            t0 = time.time()

            # waiting to receive ack
            while time_elapsed < timeout_time:
                try:
                    ack_pack, server_address = client_socket.recvfrom(4000)
                except socket.error:
                    pass
                time_elapsed = time.time() - t0
        return ack_pack

    def StopAndWait(self):
        client_socket = socket(AF_INET, SOCK_DGRAM)
        img_byte_arr = Sender.form_image_bytes(self)

        counter = 0
        ack_pack = sender2.SendAndWait(img_byte_arr, client_socket, counter)

        # check ack is not none
        if ack_pack is not None:
            # make sure the ack is for the correct packet
            sequence_number = ack_pack[0:2]

            if self.sequenceNumber == sequence_number:
                pass
            else:
                print("error")
        else:
            # ack not received
            sender2.SendAndWait()

        counter += 1


if __name__ == "__main__":
    sender2 = Sender2()
    sender2.StopAndWait()
