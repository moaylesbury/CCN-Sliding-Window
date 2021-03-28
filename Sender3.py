# Michael Aylesbury s1751472

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

        # create UDP client socket
        client_socket = socket(AF_INET, SOCK_DGRAM)
        # set socket blocking to false
        # this stops the recvfrom function from waiting until a packet is received, and instead just checks
        client_socket.setblocking(False)

        # form image bytes
        img_byte_arr = sender3.form_image_bytes()

        eof = False                             #
        end_of_window = self.window_size        #
        window_first_seq_no = 0                 #
        seq_no = 0                              #
        counter = 0                             # for indexing image bytes

        base = 0                                #
        next_seq_no = 0                         #
        t0 = 0                                  #
        begin_time = time.time()                #

        # while not received end of file flag
        while not eof:

            # initialise received to False
            received = False
            # initialise ack sequence number to 0
            ack_seq_no = 0

            # if sequence number is within window
            if next_seq_no < base + self.window_size:
                # set self sequence number to the variable seq_no, in bytes
                self.sequenceNumber = next_seq_no.to_bytes(2, 'big')
                # send next sequenceth packet with self.sequenceNumber
                sender3.send(client_socket, img_byte_arr[next_seq_no])

                # if sequence number is equal to the base number, start timer
                if base == next_seq_no:
                    t0 = time.time()

                # increment sequence number
                next_seq_no += 1

            # if timer times out
            if time.time() - t0 >= self.retry_timeout:
                # restart timer
                t0 = time.time()
                # set sequence number to base, which resends window upon next loops
                next_seq_no = base
                # set received to False
                received = False

            # try to receive from socket
            try:
                # if successful, retrieve ack packet and server address
                ack_pack, server_address = client_socket.recvfrom(4000)
                # parse the sequence number from the header of the packet
                ack_seq_no = ack_pack[0:2]
                # set received
                received = True
            # if not catch error
            except error:
                # set received to False
                received = False
                pass

            # if received is True
            if received:
                # convert ack sequence number from bytes
                ack_seq_no = int.from_bytes(ack_seq_no, 'big')
                # increment base number
                base = ack_seq_no + 1

                # if sequence number is equal to base
                if base == next_seq_no:
                    # stop timer
                    t0 = 0
                else:
                    # otherwise start timer
                    t0 = time.time()

            # check if EOF flag is 1, if so set eof True
            if self.EOF == (1).to_bytes(1, 'big'):
                eof = True

        # close client socket
        client_socket.close()
        # calculated elapsed time
        time_elapsed = time.time() - begin_time

        # print throughput: file size / time taken to send file
        print(self.fileSize / time_elapsed)

if __name__ == "__main__":
    sender3 = Sender3()
    sender3.GoBackN()