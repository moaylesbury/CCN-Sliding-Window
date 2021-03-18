from Receiver1 import Receiver
from socket import *

def increment_seq_no(s):
    return 0 if s == 1 else 1

# extending Receiver
class Receiver2(Receiver):
    def __init__(self):
        super(Receiver2, self).__init__()

    def SendAck(self, server_socket, state):
        # forming ack packet, 2 bytes containing sequence number
        ack_pack = state.to_bytes(2, 'big')  # does this have to be a byte arr?
        # make sure not none
        # server_socket.sendto(ack_pack, (self.clientAddress[0], int(self.serverPort)))
        server_socket.sendto(ack_pack, self.clientAddress)
        print(self.serverPort)

    def StopAndWait(self):
        server_socket = socket(AF_INET, SOCK_DGRAM)
        server_socket.bind(("", int(self.serverPort)))

        print("The server is ready to receive")

        counter = 0
        data = None
        seq_no = 0

        # while not self.EOF:
        while True:
            img_bytes = None

            # receive packet and extract data and sequence number
            while img_bytes is None:

                img_bytes, sequence_number = receiver2.Receive(server_socket)


            # if the sequence number is not correct, send ack for the opposite
            if seq_no == int.from_bytes(sequence_number, "big"):
                data = receiver2.append_data(data, img_bytes)
                receiver2.SendAck(server_socket, seq_no)
                seq_no = increment_seq_no(seq_no)
                print("correct packet")
            else:
                receiver2.SendAck(server_socket, increment_seq_no(seq_no))




        print("HOST RECVD: ", counter, " PACKETS")


        # write to file        TODO: does this need to be a separate function
        f = open(self.fileName, "w+b")
        f.write(bytearray(data))

        f.close()
        server_socket.close()


if __name__ == "__main__":
    receiver2 = Receiver2()
    receiver2.StopAndWait()