from Sender3 import Sender3
from socket import *
import time

class Sender4(Sender3):
    
    def __init__(self):
        super(Sender4, self).__init__()

    def shuffle_buffer(self, timers):
        for i in range(self.window_size):
            if i == self.window_size - 1:
                timers[i] = 0
            else:
                timers[i] = timers[i + 1]
        return timers

    def shift_timers(self, timers):
        for i in range(self.window_size):
            print("got here")
            if i == self.window_size - 1:
                timers[i] = True
            else:
                timers[i] = timers[i + 1]
        return timers

    def SelectiveRepeat(self):
        client_socket = socket(AF_INET, SOCK_DGRAM)
        client_socket.setblocking(False)
        img_byte_arr = sender4.form_image_bytes()   # TODO: len approx 880

        eof = False
        base = 0
        next_seq_no = 0

        counter = 0
        timers = []
        for i in range(self.window_size):
            timers.append(0)

        while not eof:
            ack_seq_no = -1
            print("sequence number: ", next_seq_no)
            print("base number    : ", base)
            if next_seq_no < base + self.window_size:   # TODO: remember to modulo
                self.sequenceNumber = next_seq_no.to_bytes(2, 'big')
                sender4.send(client_socket, img_byte_arr[counter])
                timers[next_seq_no % self.window_size] = time.time()


            for t in range(len(timers)):
                if time.time() - timers[t] >= self.retry_timeout and timers[t] != 0:
                    print("+++++timeout+++++")
                    timers[t] = time.time()
                    # next_seq_no = base

                    # go
                    if t == (next_seq_no % self.window_size):
                        self.sequenceNumber = next_seq_no.to_bytes(2, "big")
                    elif t < next_seq_no:
                        self.sequenceNumber = (next_seq_no + ((next_seq_no % self.window_size)-t)).to_bytes(2, 'big')
                    elif t > next_seq_no:
                        self.sequenceNumber = (next_seq_no + (t-(next_seq_no % self.window_size))).to_bytes(2, 'big')
                    print("RESENT: ", int.from_bytes(self.sequenceNumber, "big"))
                    sender4.send(client_socket, img_byte_arr[counter - (len(timers) - i)])


            try:
                ack_pack, server_address = client_socket.recvfrom(4000)
                ack_seq_no = ack_pack[0:2]
                ack_seq_no = int.from_bytes(ack_seq_no, 'big')
                print("received ACK ", ack_seq_no)
                timers[ack_seq_no % self.window_size] = 1
            except error:
                pass



            print("oi oi ! ", next_seq_no, " and recvd ", ack_seq_no)
            if next_seq_no == ack_seq_no:
                print("yes")
                next_seq_no += 1
                base += 1
                shuffle_amount = 0
                for t in range(self.window_size):
                    if timers[t] == 1:
                        base += 1
                        shuffle_amount += 1
                    else:
                        break
                for i in range(shuffle_amount):
                    timers = sender4.shuffle_buffer(timers)




            if self.EOF == (1).to_bytes(1, 'big'):  # TODO: can only end if this is acknowledged
                eof = True

if __name__ == "__main__":
    sender4 = Sender4()
    sender4.SelectiveRepeat()