from Sender1 import Sender
from Sender2 import Sender2
from socket import *
import sys
import time

class Sender3(Sender2):
    def __init__(self):
        super(Sender3, self).__init__()
        self.retry_timeout = float(sys.argv[4])/1000    # milliseconds to seconds
        self.window_size = int(sys.argv[5])

    def increment_seq_no(self, seq_no):
        return (seq_no + 1) % self.window_size

    def GoBackN(self):
        client_socket = socket(AF_INET, SOCK_DGRAM)
        client_socket.setblocking(False)
        img_byte_arr = sender3.form_image_bytes()

        eof = False
        end_of_window = self.window_size
        window_first_seq_no = 0
        seq_no = 0

        counter = 0     # for indexing image bytes




        base = 0
        next_seq_no = 0
        t0 = 0
        begin_time = time.time()

        while not eof:
            received = False
            ack_seq_no = 0
            print("sequence number: ", next_seq_no)
            print("base number    : ", base)

            print("a")
            if next_seq_no < base + self.window_size:   # TODO: remember to modulo
                self.sequenceNumber = next_seq_no.to_bytes(2, 'big')
                sender3.send(client_socket, img_byte_arr[next_seq_no])
                if base == next_seq_no:
                    t0 = time.time()
                next_seq_no += 1

            if time.time() - t0 >= self.retry_timeout:  # TODO: if time expires resend entire window
                print("++++timeout++++")
                t0 = time.time()
                next_seq_no = base
                received = False

            print("recv::")
            # ack_seq_no, not_received = sender3.ReceiveAck(client_socket, 0.001)  # checks to see if any acks present
            try:
                ack_pack, server_address = client_socket.recvfrom(4000)
                ack_seq_no = ack_pack[0:2]
                received = True
                print("received")
            except error:
                received = False
                print("error")
                pass

            print("done")
            print("b")

            if received:
                print("c")
                ack_seq_no = int.from_bytes(ack_seq_no, 'big')
                print("received ACK ", ack_seq_no)
                base = ack_seq_no + 1     #TODO: make sure this is the right number
                if base == next_seq_no:
                    t0 = 0
                else:
                    t0 = time.time()
            print("d")
            if self.EOF == (1).to_bytes(1, 'big'):  # TODO: can only end if this is acknowledged
                eof = True

        time_elapsed = time.time() - begin_time
        print(self.fileSize / time_elapsed)

if __name__ == "__main__":
    sender3 = Sender3()
    sender3.GoBackN()