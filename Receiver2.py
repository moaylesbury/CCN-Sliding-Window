# Michael Aylesbury s1751472

from Receiver1 import Receiver
from socket import *


def increment_seq_no(s):
    return 0 if s == 1 else 1


class Receiver2(Receiver):
    def __init__(self):
        # inherit super self variables
        super(Receiver2, self).__init__()

    def SendAck(self, server_socket, state):
        # forming ack packet, 2 bytes containing sequence number
        ack_pack = state.to_bytes(2, 'big')  # does this have to be a byte arr?
        # make sure not none
        # server_socket.sendto(ack_pack, (self.clientAddress[0], int(self.serverPort)))
        server_socket.sendto(ack_pack, self.clientAddress)

    def StopAndWait(self):
        # create UDP server socket
        server_socket = socket(AF_INET, SOCK_DGRAM)
        # bind socket to server port
        server_socket.bind(("", int(self.serverPort)))

        # initialise counter to 0
        counter = 0
        # initialise data to None
        data = None
        # initialise seq_no to 0
        seq_no = 0
        # initialise EOF to 0
        self.EOF = (0).to_bytes(1, "big")

        # while not received end of file flag
        while self.EOF == (0).to_bytes(1, "big"):
            # initialise img_bytes to None
            img_bytes = None

            # loop until img_bytes are received
            while img_bytes is None:
                # receive packet and extract data and sequence number
                img_bytes, sequence_number = receiver2.Receive(server_socket)


            # if the sequence number is not correct, send ack for the opposite
            if seq_no == int.from_bytes(sequence_number, "big"):
                data = receiver2.append_data(data, img_bytes)
                receiver2.SendAck(server_socket, seq_no)
                seq_no = increment_seq_no(seq_no)
            else:
                # otherwise send ack for the correct sequence number
                receiver2.SendAck(server_socket, increment_seq_no(seq_no))

        receiver2.WriteDataCloseSocket(data, server_socket)


if __name__ == "__main__":
    receiver2 = Receiver2()
    receiver2.StopAndWait()
