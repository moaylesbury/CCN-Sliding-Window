from Receiver3 import Receiver3
from socket import *

class Receiver4(Receiver3):
    def __init__(self):
        super(Receiver4, self).__init__()

    def shuffle_buffer(self, buffer):
        for i in range(self.window_size):
            if i == self.window_size - 1:
                buffer[i] = 0
            else:
                buffer[i] = buffer[i + 1]
        return buffer

    def SelectiveRepeat(self):
        print(self.window_size)
        server_socket = socket(AF_INET, SOCK_DGRAM)
        server_socket.bind(("", int(self.serverPort)))

        # initialising buffer
        buffer = []
        for i in range(self.window_size):
            buffer.append(0)
        #######
        base = 0
        received_seq_no = []

        expected_seq_no = 0
        data = None
        self.EOF = (0).to_bytes(1, "big")
        while self.EOF == (0).to_bytes(1, "big"):
            print("expected seq no: ", expected_seq_no)
            print("base: ", base)

            img_bytes, seq_no = receiver4.Receive(server_socket)
            print("received")
            seq_no = int.from_bytes(seq_no, 'big')
            # TODO: check in window
            if seq_no < base + self.window_size:
                buffer[seq_no % self.window_size] = img_bytes
            # if seq_no not in received_seq_no:
            #     received_seq_no.append(seq_no)
            #     buffer.append(img_bytes)

            receiver4.SendAck(server_socket, seq_no)

            # dealing with buffer

            shuffle_amount = base
            for b in range(self.window_size):
                if buffer[b] != 0:
                    print("yea!!!!!!")
                    base += 1
                    data = receiver4.append_data(data, img_bytes)
                else:
                    print("BROKEN")
                    break
            shuffle_amount = base - shuffle_amount
            for i in range(shuffle_amount):
                buffer = receiver4.shuffle_buffer(buffer)  # TODO: shuffle buffer








            # if expected_seq_no in received_seq_no:
            #
            #     for i in range(len(buffer)):
            #         print(i)
            #         if received_seq_no[i] == expected_seq_no:
            #             print("MATCHMATCH")
            #             print(expected_seq_no)
            #             expected_seq_no = (expected_seq_no + 1) % self.window_size
            #             data = receiver4.append_data(data, img_bytes)
            #             buffer.pop(i)
            #             received_seq_no.pop(i)
            #             break





        # write to file        TODO: does this need to be a separate function
        f = open(self.fileName, "w+b")
        f.write(bytearray(data))

        f.close()
        server_socket.close()




if __name__ == "__main__":
    receiver4 = Receiver4()
    receiver4.SelectiveRepeat()