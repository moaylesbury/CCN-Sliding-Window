from Receiver3 import Receiver3
from socket import *

class Receiver4(Receiver3):
    def __init__(self):
        super(Receiver3, self).__init__()

    def process_buffer(self, buffer, data):
        counter = 0
        receiver4.append_data(data, image_bytes=)
        return []
    def SelectiveRepeat(self):

        server_socket = socket(AF_INET, SOCK_DGRAM)
        server_socket.bind(("", int(self.serverPort)))

        buffer = []

        expected_seq_no = 0
        data = None
        self.EOF = (0).to_bytes(1, "big")
        while self.EOF == (0).to_bytes(1, "big"):
            print("expected seq no: ", expected_seq_no)


            img_bytes, seq_no = receiver4.Receive(server_socket)
            print("received")
            seq_no = int.from_bytes(seq_no, 'big')

            if seq_no == expected_seq_no:
                data = receiver4.append_data(data, img_bytes)
                receiver4.SendAck(server_socket, seq_no)
                print("sent ack")
                expected_seq_no += 1
            else:
                receiver4.SendAck(server_socket, expected_seq_no-1)

        # write to file        TODO: does this need to be a separate function
        f = open(self.fileName, "w+b")
        f.write(bytearray(data))

        f.close()
        server_socket.close()




if __name__ == "__main__":
    receiver4 = Receiver4()
    receiver4.SelectiveRepeat()