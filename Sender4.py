# Michael Aylesbury s1751472

from Sender3 import Sender3
from socket import *
import time


class Sender4(Sender3):
    
    def __init__(self):
        # inherit super self variables
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

        # create UDP client socket
        client_socket = socket(AF_INET, SOCK_DGRAM)
        # set socket blocking to false
        # this stops the recvfrom function from waiting until a packet is received, and instead just checks
        client_socket.setblocking(False)

        # form image bytes
        img_byte_arr = sender4.form_image_bytes()

        eof = False
        base = 0
        next_seq_no = 0

        to_remove = []

        ## for testing
        resent = []
        acks_received = []
        tpos = []
        ##

        counter = 0
        timers = {}
        # for i in range(self.window_size):
        #     timers.append(0)

        begin_time = time.time()

        # while not received end of file flag
        while not eof:
            ack_seq_no = -1

            print("")
            print("")
            print("|-         base=%s         -|" % base)
            print("")
            print("-----acks received-----")
            print(acks_received)
            print("a")
            if base <= next_seq_no < base + self.window_size:   # TODO: remember to modulo
                self.sequenceNumber = next_seq_no.to_bytes(2, 'big')
                print("*sending: ", next_seq_no)
                sender4.send(client_socket, img_byte_arr[next_seq_no])
                timers[next_seq_no] = time.time()
                next_seq_no += 1
            print("b")
            for t in timers.keys():
                if base <= t < base + self.window_size:
                    if time.time() - timers[t] >= self.retry_timeout and timers[t] != 0:
                        print("+++++timeout+++++")
                        print("thus resending %s" % t)
                        timers[t] = time.time()
                        self.sequenceNumber = t.to_bytes(2, 'big')
                        sender4.send(client_socket, img_byte_arr[t])
                else:
                    to_remove.append(t)
            print("c")
            # doing some cleaning up to save cpu
            if len(to_remove) > 0:
                for t in to_remove:
                    if t in timers.keys():
                        del timers[t]
            print("d")
            try:
                ack_pack, server_address = client_socket.recvfrom(4000)
                ack_seq_no = ack_pack[0:2]
                ack_seq_no = int.from_bytes(ack_seq_no, 'big')
                if ack_seq_no not in acks_received:
                    acks_received.append(ack_seq_no)
                while base in acks_received:
                    base += 1
            except error:
                pass
            print("e")


            # time.sleep(2)

            if self.EOF == (1).to_bytes(1, 'big'):  # TODO: can only end if this is acknowledged
                eof = True

        time_elapsed = time.time() - begin_time
        print(time_elapsed)
        # print(self.fileSize / time_elapsed)

if __name__ == "__main__":
    sender4 = Sender4()
    # arr = [0, 1, 2, 3, 4]
    # test = sender4.shuffle_buffer(arr)
    # print(test)
    sender4.SelectiveRepeat()
