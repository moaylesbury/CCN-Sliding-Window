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

    def retrans_seq_no(self, t, next_seq_no):
        self.sequenceNumber = (next_seq_no - (self.window_size - t)).to_bytes(2, 'big')
        # self.sequenceNumber = (next_seq_no + (t - (next_seq_no % self.window_size))).to_bytes(2, 'big')

    def SelectiveRepeat(self):
        client_socket = socket(AF_INET, SOCK_DGRAM)
        client_socket.setblocking(False)
        img_byte_arr = sender4.form_image_bytes()   # TODO: len approx 880

        eof = False
        base = 0
        next_seq_no = 0

        ## for testing
        resent = []
        acks_received = []
        tpos = []
        ##

        counter = 0
        timers = []
        for i in range(self.window_size):
            timers.append(0)

        while not eof:
            print(timers)
            ack_seq_no = -1
            print("sequence number: ", next_seq_no)
            print("base number    : ", base)
            print("RESENT PACKETS: ", resent)
            print("T POS: ", tpos)
            print("ACKS RECEIVED: ", acks_received)

            # sendpacket
            # -if between base and base + window size
            # --send packet
            # --increase next_seq_num
            # --start timer
            if base <= next_seq_no < base + self.window_size:   # TODO: remember to modulo
                self.sequenceNumber = next_seq_no.to_bytes(2, 'big')
                sender4.send(client_socket, img_byte_arr[counter])
                timers[next_seq_no % self.window_size] = time.time()
                next_seq_no += 1

            # check timers
            # - if any timer has expired
            # --resend packet with corresponding sequence number
            # --start its timer
            for t in range(len(timers)):
                if time.time() - timers[t] >= self.retry_timeout and timers[t] != 0:
                    print("+++++timeout+++++")
                    timers[t] = time.time()
                    sender4.retrans_seq_no(t, next_seq_no) # changes sequence number
                    sender4.send(client_socket, img_byte_arr[counter - (len(timers) - i)])
                    print("RESENT: ", int.from_bytes(self.sequenceNumber, "big"))
                    resent.append(int.from_bytes(self.sequenceNumber, "big"))
                    tpos.append(t)

            # receive ack
            # - if ack_seq_num == next_seq_num - 1
            # --base += 1
            # --shuffle timers
            # --loop through timers
            # --- if timer = 1
            # ---base += 1
            # ---shuffle timers
            # -- else
            # ---break
            # -elif between base and base + window size
            # --timer = 1
            print("dsagjalsdkhkasnhklasklhnadh")
            print("dsagjalsdkhkasnhklasklhnadh")
            print("dsagjalsdkhkasnhklasklhnadh")
            print("dsagjalsdkhkasnhklasklhnadh")
            print("dsagjalsdkhkasnhklasklhnadh")
            try:
                ack_pack, server_address = client_socket.recvfrom(4000)
                ack_seq_no = ack_pack[0:2]
                ack_seq_no = int.from_bytes(ack_seq_no, 'big')
                print("=-=-=-=-=--=-=-=--=-=-=-=-=-=-=-=-=--=-=-=--=-=-=-=-=-=-=-=-=--=-=-=--=-=-=-=-")
                print("=-=-=-=-=--=-=-=--=-=-=-=-=-=-=-=-=--=-=-=--=-=-=-=-=-=-=-=-=--=-=-=--=-=-=-=-")
                print("=-=-=-=-=--=-=-=--=-=-=-=-=-=-=-=-=--=-=-=--=-=-=-=-=-=-=-=-=--=-=-=--=-=-=-=-")
                print("ACK SQN: ", ack_seq_no, " NEXT SQN - 1: ", next_seq_no)
                print("=-=-=-=-=--=-=-=--=-=-=-=-=-=-=-=-=--=-=-=--=-=-=-=-=-=-=-=-=--=-=-=--=-=-=-=-")
                print("=-=-=-=-=--=-=-=--=-=-=-=-=-=-=-=-=--=-=-=--=-=-=-=-=-=-=-=-=--=-=-=--=-=-=-=-")
                print("=-=-=-=-=--=-=-=--=-=-=-=-=-=-=-=-=--=-=-=--=-=-=-=-=-=-=-=-=--=-=-=--=-=-=-=-")
                if ack_seq_no not in acks_received:
                    acks_received.append(ack_seq_no)
                if ack_seq_no == next_seq_no - 1:
                    base += 1
                    timers = sender4.shuffle_buffer(timers) # stops timer
                    for t in range(self.window_size):
                        if timers[t] == 1:
                            print("over here! ", timers)
                            base += 1
                            timers = sender4.shuffle_buffer(timers)
                        else:
                            break
                elif base <= ack_seq_no < base + self.window_size:
                    timers[ack_seq_no % self.window_size] = 1

                print("received ACK ", ack_seq_no)
            except error:
                pass

            # check timers
            # - if any timer has expired
            # --resend packet with corresponding sequence number
            # --start its timer

            # print("oi oi ! ", next_seq_no, " and recvd ", ack_seq_no)
            # if next_seq_no == ack_seq_no:
            #     print("yes")
            #     next_seq_no += 1
            #     base += 1
            #     shuffle_amount = 0
            #     for t in range(self.window_size):
            #         if timers[t] == 1:
            #             base += 1
            #             next_seq_no += 1
            #             shuffle_amount += 1
            #         else:
            #             break
            #     for i in range(shuffle_amount):
            #         timers = sender4.shuffle_buffer(timers)
            #



            if self.EOF == (1).to_bytes(1, 'big'):  # TODO: can only end if this is acknowledged
                eof = True

if __name__ == "__main__":
    sender4 = Sender4()
    sender4.SelectiveRepeat()
    # sender4.retrans_seq_no()