from Sender3 import Sender3
from socket import *
import time

class Sender4(Sender3):
    
    def __init__(self):
        super(Sender4, self).__init__()

    def SelectiveRepeat(self):
        client_socket = socket(AF_INET, SOCK_DGRAM)
        client_socket.setblocking(False)
        img_byte_arr = sender4.form_image_bytes()

        eof = False
        base = 0
        next_seq_no = 0
        t0 = 0

        counter = 0

        # initialise array
        timers = []
        for i in self.window_size:
            timers.append(0)
        print(timers)

        while not eof:
            if next_seq_no < base + self.window_size:   # TODO: remember to modulo
                self.sequenceNumber = next_seq_no.to_bytes(2, 'big')
                sender4.send(client_socket, img_byte_arr[next_seq_no])
                if base == next_seq_no:
                    timers[next_seq_no % self.window_size] = time.time()
                next_seq_no += 1
                counter += 1

            for t in range(len(timers)):
                if time.time() - timers[t] >= self.retry_timeout:
                    print("++++timeout++++")
                    timers[t] = time.time()
                    next_seq_no = base
                    counter -= next_seq_no % self.window_size
                    sender4.send(client_socket, img_byte_arr[counter])

            print("recv::")
            try:
                ack_pack, server_address = client_socket.recvfrom(4000)
                ack_seq_no = ack_pack[0:2]
                received = True
                print("received")
            except error:
                received = False
                print("error")
                pass

            if received:
                ack_seq_no = int.from_bytes(ack_seq_no, 'big')
                print("received ACK ", ack_seq_no)
                base = ack_seq_no + 1     #TODO: make sure this is the right number
                if base == next_seq_no:
                    timers[next_seq_no % self.window_size] = 0
                else:
                    timers[next_seq_no % self.window_size] = time.time()

            # can only move on if all timers are stopped
            acked = True
            ack_count = 0
            while acked:



            print("done")


            if self.EOF == (1).to_bytes(1, 'big'):  # TODO: can only end if this is acknowledged
                eof = True

if __name__ == "__main__":
    sender4 = Sender4()
    sender4.SelectiveRepeat()