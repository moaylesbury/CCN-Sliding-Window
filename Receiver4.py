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
        server_socket = socket(AF_INET, SOCK_DGRAM)
        server_socket.bind(("", int(self.serverPort)))

        # initialising buffer
        buffer = []
        data_buffer = {}
        for i in range(self.window_size):
            buffer.append(0)
        #######
        base = 0

        seq_nos_received = []

        expected_seq_no = 0
        data = None
        self.EOF = (0).to_bytes(1, "big")

        while self.EOF == (0).to_bytes(1, "big"):
            print("expected seq no: ", expected_seq_no)
            print("base: ", base)
            print("seq nos received: ", seq_nos_received)

            img_bytes, seq_no = receiver4.Receive(server_socket)
            seq_no = int.from_bytes(seq_no, 'big')
            buffer[seq_no % self.window_size] = img_bytes
            data_buffer[seq_no] = img_bytes
            receiver4.SendAck(server_socket, seq_no)

            if seq_no not in seq_nos_received:
                seq_nos_received.append(seq_no)

            print("RECIEVED : : : ", seq_no)


            while base in seq_nos_received:
                data = receiver4.append_data(data, data_buffer[base])
                buffer = receiver4.shuffle_buffer(buffer)
                base += 1
















            # if seq_no == expected_seq_no:
            #     expected_seq_no += 1
            #     print("Base increase as ", seq_no, " == ", expected_seq_no)
            #     base += 1
            #     data = receiver4.append_data(data, img_bytes)
            #     receiver4.SendAck(server_socket, seq_no)
            #     buffer = receiver4.shuffle_buffer(buffer)
            #
            #     shuffle_amount = 0
            #     for b in range(1, self.window_size):
            #         if buffer[b] != 0:
            #             # print("base increase because")
            #             base += 1
            #             shuffle_amount += 1
            #             expected_seq_no += 1
            #             data = receiver4.append_data(data, img_bytes)
            #         else:
            #             break
            #     for i in range(shuffle_amount):
            #         buffer = receiver4.shuffle_buffer(buffer)
            #

            # elif seq_no < base + self.window_size:
            #     buffer[seq_no % self.window_size] = img_bytes
            #     receiver4.SendAck(server_socket, seq_no)
            #
            #












        # write to file        TODO: does this need to be a separate function
        f = open(self.fileName, "w+b")
        f.write(bytearray(data))

        f.close()
        server_socket.close()






if __name__ == "__main__":
    receiver4 = Receiver4()
    receiver4.SelectiveRepeat()


    # testing
    # tester = [1,2,0,3,0]
    # print("tester before: ", tester)
    # shuffle_amount = 0
    # base = 0
    # for b in range(5):
    #     if tester[b] != 0:
    #         base += 1
    #         shuffle_amount += 1
    #     else:
    #         break
    # for i in range(shuffle_amount):
    #     tester = receiver4.shuffle_buffer(tester)
    # print("tester after: ", tester)
    # print('base: ', base)
    # print("shuffle amount: ", shuffle_amount)




