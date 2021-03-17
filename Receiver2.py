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

        print("The server is ready to receive")

        # State 0
        counter = 0
        data = None
        state = 0            # denote s
        opposite_state = 1   # denote o
        temp = 0

        while not self.EOF:

            # receive packet and extract data and sequence number
            img_bytes, sequence_number = receiver2.Receive(server_socket, data)

            # s -> s: receive packet with sequence number o
            # send ack with sequence number o
            receiver2.SendAck(server_socket, no=opposite_state)

            # s -> o: receive packet with sequence number s
            # append data
            Receiver.append_data(data, img_bytes)
            # send ack with sequence number s
            receiver2.SendAck(server_socket, no=state)

            # move to state o
            temp = state
            state = opposite_state
            opposite_state = temp


        print("HOST RECVD: ", counter, " PACKETS")


        # write to file        TODO: does this need to be a separate function
        f = open(self.fileName, "w+b")
        f.write(bytearray(data))

        f.close()
        server_socket.close()


if __name__ == "__main__":
    receiver2 = Receiver2()