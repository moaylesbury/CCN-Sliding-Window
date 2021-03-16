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

        counter = 0
        data = None
        while not self.EOF:
            data = self.Receive(server_socket, data)
            self.SendAck(server_socket)
        print("HOST RECVD: ", counter, " PACKETS")
        f = open(self.fileName, "w+b")
        f.write(bytearray(data))

        f.close()
        server_socket.close()


if __name__ == "__main__":
    Receiver2()