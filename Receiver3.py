# Michael Aylesbury s1751472

from Receiver2 import Receiver2
from socket import *


class Receiver3(Receiver2):
    def __init__(self):
        # inherit super self variables
        super(Receiver3, self).__init__()

    def GoBackN(self):
        # create UDP server socket
        server_socket = socket(AF_INET, SOCK_DGRAM)
        # bind socket to server port
        server_socket.bind(("", int(self.serverPort)))

        # initialise expected sequence number to 0
        expected_seq_no = 0
        # initialise data to None
        data = None
        # initialise EOF to 0
        self.EOF = (0).to_bytes(1, "big")

        # while not received end of file flag
        while self.EOF == (0).to_bytes(1, "big"):

            # receive packet and extract data and sequence number
            img_bytes, seq_no = receiver3.Receive(server_socket)
            # convert sequence number from bytes
            seq_no = int.from_bytes(seq_no, 'big')

            # if the seqeuence number is equal to the expected sequence number
            if seq_no == expected_seq_no:
                # append data
                data = receiver3.append_data(data, img_bytes)
                # send ack
                receiver3.SendAck(server_socket, seq_no)
                # increment expected sequence nubmer
                expected_seq_no += 1
            else:
                # otherwise send ack from expected sequence number - 1
                receiver3.SendAck(server_socket, expected_seq_no-1)

        # open file to write bytes
        f = open(self.fileName, "w+b")
        # write bytearray of data to file
        f.write(bytearray(data))

        # close file
        f.close()
        # close socket
        server_socket.close()


if __name__ == "__main__":
    receiver3 = Receiver3()
    receiver3.GoBackN()
