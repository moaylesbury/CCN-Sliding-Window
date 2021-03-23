from Sender3 import Sender3
from socket import *
import time

class Sender4(Sender3):
    
    def __init__(self):
        super(Sender4, self).__init__()

    def shuffle_buffer(self, timers):
        for i in range(self.window_size):
            if i == self.window_size - 1:
                timers[i] = time.time()
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
        timers = {}
        # for i in range(self.window_size):
        #     timers.append(0)

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
                sender4.send(client_socket, img_byte_arr[next_seq_no])
                timers[next_seq_no] = time.time()
                next_seq_no += 1

            # check timers
            # - if any timer has expired
            # --resend packet with corresponding sequence number
            # --start its timer
            print(len(timers))
            print(timers)
            for t in timers.keys():

                if t >= base and t < base + self.window_size:
                    if time.time() - timers[t] >= self.retry_timeout and timers[t] != 0:
                        print("+++++timeout+++++")
                        timers[t] = time.time()
                        # sender4.retrans_seq_no(t, next_seq_no) # changes sequence number
                        # sender4.send(client_socket, img_byte_arr[next_seq_no - 1 - (self.window_size - t)]) # -1?
                        self.sequenceNumber = t.to_bytes(2, 'big')
                        sender4.send(client_socket, img_byte_arr[t])
                        print("RESENT: ", int.from_bytes(self.sequenceNumber, "big"))
                        resent.append(int.from_bytes(self.sequenceNumber, "big"))
                        tpos.append(t)



            try:
                ack_pack, server_address = client_socket.recvfrom(4000)
                ack_seq_no = ack_pack[0:2]
                ack_seq_no = int.from_bytes(ack_seq_no, 'big')
                print("=-=-=-=-=--=-=-=--=-=-=-=-=-=-=-=-=--=-=-=--=-=-=-=-=-=-=-=-=--=-=-=--=-=-=-=-")
                print("ACK SQN: ", ack_seq_no, " NEXT SQN - 1: ", next_seq_no)
                print("=-=-=-=-=--=-=-=--=-=-=-=-=-=-=-=-=--=-=-=--=-=-=-=-=-=-=-=-=--=-=-=--=-=-=-=-")
                if ack_seq_no not in acks_received:
                    acks_received.append(ack_seq_no)

                while base in acks_received:
                    base += 1
            except error:
                pass






            if self.EOF == (1).to_bytes(1, 'big'):  # TODO: can only end if this is acknowledged
                eof = True

if __name__ == "__main__":
    sender4 = Sender4()
    sender4.SelectiveRepeat()
    # sender4.retrans_seq_no()