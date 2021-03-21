from Receiver3 import Receiver3
from socket import *

class Receiver4(Receiver3):
    def __init__(self):
        super(Receiver3, self).__init__()

    def process_buffer(self, buffer, data, img_bytes):
        counter = 0
        receiver4.append_data(data, img_bytes)

        return []
    def SelectiveRepeat(self):

        server_socket = socket(AF_INET, SOCK_DGRAM)
        server_socket.bind(("", int(self.serverPort)))

        buffer = []
        received_ack = []

        expected_seq_no = 0
        data = None
        self.EOF = (0).to_bytes(1, "big")
        while self.EOF == (0).to_bytes(1, "big"):
            print("expected seq no: ", expected_seq_no)
            print("buffer size: ", len(buffer))

            img_bytes, seq_no = receiver4.Receive(server_socket)
            print("received")
            seq_no = int.from_bytes(seq_no, 'big')

            received_ack.append(True)
            buffer.append(img_bytes)

            receiver4.SendAck(server_socket, seq_no)
            print("sent ack")
            expected_seq_no += 1

            # dealing with buffer
            got_last_ack = True
            for i in range(len(buffer)):
                if received_ack[i] and got_last_ack:
                    data = receiver4.append_data(data, img_bytes)
                    buffer.pop(i)
                    received_ack.pop(i)
                else:
                    got_last_ack = False




        # write to file        TODO: does this need to be a separate function
        f = open(self.fileName, "w+b")
        f.write(bytearray(data))

        f.close()
        server_socket.close()




if __name__ == "__main__":
    receiver4 = Receiver4()
    receiver4.SelectiveRepeat()