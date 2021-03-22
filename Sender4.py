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
        t0 = 0

        counter = 0
        temp = 0
        received = False
        # initialise array
        timers = []
        acks_received = []
        print()
        for i in range(self.window_size):
            timers.append(0)
            acks_received.append(False)

        while not eof:
            print("sequence number: ", next_seq_no)
            print("base number    : ", base)
            if next_seq_no < base + self.window_size:   # TODO: remember to modulo
                self.sequenceNumber = next_seq_no.to_bytes(2, 'big')
                sender4.send(client_socket, img_byte_arr[counter])
                timers[next_seq_no % self.window_size] = time.time()
                next_seq_no += 1

            print("b")
            temp = counter
            for t in range(len(timers)):
                print("normalised time: ", time.time() - timers[t])
                if time.time() - timers[t] >= self.retry_timeout and timers[t] != 0:
                    print("normalised time: ")
                    print("++++timeout++++")
                    timers[t] = time.time()
                    # next_seq_no = base

                    # go
                    if t == (next_seq_no % self.window_size):
                        self.sequenceNumber = next_seq_no.to_bytes(2, "big")
                    elif t < next_seq_no:
                        self.sequenceNumber = (next_seq_no + ((next_seq_no % self.window_size)-t)).to_bytes(2, 'big')
                    elif t > next_seq_no:
                        self.sequenceNumber = (next_seq_no + (t-(next_seq_no % self.window_size))).to_bytes(2, 'big')

                    # TODO: reset counter after
                    sender4.send(client_socket, img_byte_arr[counter - (len(timers) - i)])

            counter = temp

            try:
                ack_pack, server_address = client_socket.recvfrom(4000)
                ack_seq_no = ack_pack[0:2]
                received = True
            except error:
                received = False
                pass

            if received:
                ack_seq_no = int.from_bytes(ack_seq_no, 'big')
                print("received ACK ", ack_seq_no)
                timers[ack_seq_no % self.window_size] = 1
                acks_received[ack_seq_no % self.window_size] = True

            shuffle_amount = 0
            for t in range(self.window_size):
                if timers[t] == 1:
                    base += 1
                    shuffle_amount += 1
                else:
                    print("BROKEN")
                    break
            for i in range(shuffle_amount):
                timers = sender4.shuffle_buffer(timers)



            # for i in range(len(acks_received)):
            #     if i < next_seq_no % self.window_size:
            #         if not acks_received[i]:
            #             self.sequenceNumber = (next_seq_no - (len(acks_received)-i)).to_bytes(2, 'big')
            #             sender4.send(client_socket, img_byte_arr[counter - (len(acks_received)-i)])
            #
            # if next_seq_no == base + self.window_size:



            # increase_base = True
            # inc_count = 0
            # while increase_base and inc_count < self.window_size - 1:
            #     print("¢¢¢¢¢¢¢¢¢¢¢¢¢¢¢¢¢¢¢¢¢¢¢¢¢¢¢¢¢¢")
            #     print("¢¢¢¢¢¢¢¢¢¢¢¢¢¢¢¢¢¢¢¢¢¢¢¢¢¢¢¢¢¢")
            #     print("¢¢¢¢¢¢¢¢¢¢¢¢¢¢¢¢¢¢¢¢¢¢¢¢¢¢¢¢¢¢")
            #     print(acks_received[inc_count])
            #     if acks_received[inc_count]:
            #         base += 1
            #         # [True, False, False, False, False]
            #         # [False, False, False, False, True]
            #         # as base has increased, shift entire array along one
            #         print("BEFORE: ", acks_received)
            #         all_true = True
            #         for i in range(self.window_size):
            #             print("got here")
            #             if i == self.window_size-1:
            #                 all_true = False
            #                 acks_received[i] = True
            #             else:
            #                 acks_received[i] = acks_received[i+1]
            #         print("AFTER : ", acks_received)
            #             # arr[n] = False
            #             # arr[0] = arr[1]
            #             # arr[1] = arr[2]
            #             # ...
            #             # arr[n-1] = arr[n]
            #     else:
            #         increase_base = False

                # base = ack_seq_no + 1     #TODO: make sure this is the right number



            # can only move on if all timers are stopped
            #acked = True
            # ack_count = 0
            #while acked:



            print("e")


            if self.EOF == (1).to_bytes(1, 'big'):  # TODO: can only end if this is acknowledged
                eof = True

if __name__ == "__main__":
    sender4 = Sender4()
    sender4.SelectiveRepeat()