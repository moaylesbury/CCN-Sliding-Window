from Sender1 import Sender
from Sender2 import Sender2
from socket import *
import sys
import time


class Sender3(Sender):
    def __init__(self):
        super(Sender3, self).__init__()
        self.retry_timeout = sys.argv[4]
        self.window_size = sys.argv[5]

    def increment_seq_no(self, seq_no):
        return (seq_no + 1) % self.window_size

    def GoBackN(self):
        client_socket = socket(AF_INET, SOCK_DGRAM)

        img_byte_arr = sender3.form_image_bytes()

        eof = False
        end_of_window = self.window_size
        window_first_seq_no = 0
        seq_no = 0

        counter = 0     # for indexing image bytes




        while not eof:

            if seq_no != end_of_window:
                self.sequenceNumber = seq_no
                sender3.send(client_socket, img_byte_arr[counter])
                counter += 1

            ack_seq_no, received = Sender2.ReceiveAck(client_socket, 0.01) # checks to see if any acks present

            if received:
                window_first_seq_no += 1
                t0 = time.time()

            if time.time() - t0 >= self.retry_timeout:  # TODO: if time expires resend entire window
                t0 = time.time()
                seq_no = window_first_seq_no
                counter = window_first_seq_no

            # if seq_no == end_of_window:
            #     # ack must be received for seq_no - end


            seq_no = sender3.increment_seq_no(seq_no)
            end_of_window =  seq_no + self.window_size



            if self.EOF == (1).to_bytes(1, 'big'):
                eof = True

if __name__ == "__main__":
    sender3 = Sender3()