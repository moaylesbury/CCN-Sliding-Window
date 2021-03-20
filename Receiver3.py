from Receiver1 import Receiver
from Receiver2 import Receiver2
from socket import *
import sys

class Receiver3(Receiver2):
    def __init__(self):
        super(Receiver3, self).__init__()


    def GoBackN(self):

        server_socket = socket(AF_INET, SOCK_DGRAM)
        server_socket.bind(("", int(self.serverPort)))

        expected_seq_no = 0
        data = None
        self.EOF = (0).to_bytes(1, "big")
        while self.EOF == (0).to_bytes(1, "big"):
            print("expected seq no: ", expected_seq_no)


            img_bytes, seq_no = receiver3.Receive(server_socket)
            print("received")
            seq_no = int.from_bytes(seq_no, 'big')

            if seq_no == expected_seq_no:
                data = receiver3.append_data(data, img_bytes)
                receiver3.SendAck(server_socket, seq_no)
                print("sent ack")
                expected_seq_no += 1
            else:
                receiver3.SendAck(server_socket, expected_seq_no-1)

        # write to file        TODO: does this need to be a separate function
        f = open(self.fileName, "w+b")
        f.write(bytearray(data))

        f.close()
        server_socket.close()




if __name__ == "__main__":
    receiver3 = Receiver3()
    receiver3.GoBackN()