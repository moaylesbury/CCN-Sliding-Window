from Receiver1 import Receiver
from socket import *


# extending Receiver
class Receiver2(Receiver):
    def __init__(self):
        super(Receiver2, self).__init__()

    def SendAck(self, server_socket):
        # forming ack packet, 2 bytes containing sequence number
        ack_pack = self.sequence_number.to_bytes(2, 'big')  # does this have to be a byte arr?
        # make sure not none
        server_socket.sendto(ack_pack, (self.client_address, int(self.serverPort)))

    def StopAndWait(self):
        server_socket = socket(AF_INET, SOCK_DGRAM)
        server_socket.bind(("", int(self.serverPort)))
        sequence_numbers = []

        print("The server is ready to receive")

        counter = 0
        data = None
        while not self.EOF:

            # receive packet and extract data and sequence number
            data, sequence_number = self.Receive(server_socket, data)
            self.SendAck(server_socket)

            # TODO: make receive1 not add data straight away, as we need to check for duplicates

            # check not a duplicate
            if sequence_number not in sequence_numbers:
                addData()
                sequence_numbers.append(sequence_number)
            else:
                # if a duplicate do nothing and wait for retransmit....? that doesnt sound right
                pass




        print("HOST RECVD: ", counter, " PACKETS")


        # write to file        TODO: does this need to be a separate function
        f = open(self.fileName, "w+b")
        f.write(bytearray(data))

        f.close()
        server_socket.close()


if __name__ == "__main__":
    Receiver2()