# Michael Aylesbury s1751472

from Receiver3 import Receiver3
from socket import *
import sys


class Receiver4(Receiver3):
    def __init__(self):
        super(Receiver4, self).__init__()
        self.window_size = int(sys.argv[3])

    def shuffle_buffer(self, buffer):
        for i in range(self.window_size):
            if i == self.window_size - 1:
                buffer[i] = 0
            else:
                buffer[i] = buffer[i + 1]
        return buffer

    def SelectiveRepeat(self):
        server_socket = socket(AF_INET, SOCK_DGRAM)
        server_socket.bind(("", int(self.serverPort)))


        data_buffer = {}

        base = 0


        to_remove = []

        data = None
        self.EOF = (0).to_bytes(1, "big")

        while self.EOF == (0).to_bytes(1, "big"):
            print("base: ", base)
            print("seq nos received: ", data_buffer.keys())
            print("")
            print("")
            print("|-         waiting...         -|")
            img_bytes, seq_no = receiver4.Receive(server_socket)
            seq_no = int.from_bytes(seq_no, 'big')
            data_buffer[seq_no] = img_bytes
            receiver4.SendAck(server_socket, seq_no)



            print("RECIEVED : : : ", seq_no)

            while base in data_buffer.keys() and base < base + self.window_size - 1:
                to_remove.append(base)
                data = receiver4.append_data(data, data_buffer[base])
                base += 1

            print(data_buffer.keys())

            # # doing some cleaning
            #
            # for key in to_remove:
            #     if key in data_buffer.keys():
            #         del data_buffer[key]

        # write to file
        f = open(self.fileName, "w+b")
        f.write(bytearray(data))

        f.close()
        server_socket.close()






if __name__ == "__main__":
    receiver4 = Receiver4()
    receiver4.SelectiveRepeat()






