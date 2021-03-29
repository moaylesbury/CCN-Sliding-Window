# Michael Aylesbury s1751472

from Sender1 import Sender
from socket import *
import time
import select


def increment_seq_no(s):
    return 0 if s == 1 else 1


class Sender2(Sender):
    def __init__(self):
        # inherit super self variables
        super(Sender2, self).__init__()

    def ReceiveAck(self, client_socket, timeout_time):
        # Input:  self, client_socket, timeout_time
        # Output:

        ready = select.select([client_socket], [], [], timeout_time)

        ack_pack = None
        if ready[0]:
            ack_pack, server_address = client_socket.recvfrom(4000)


        if ack_pack is None:
            return None, True
        else:
            seq_num = ack_pack[0:2]
            return seq_num, False       # as timed out

    def StopAndWait(self):
        # Input:  self
        # Output:

        # create UDP client socket
        client_socket = socket(AF_INET, SOCK_DGRAM)
        # set socket blocking to false
        # this stops the recvfrom function from waiting until a packet is received, and instead just checks
        client_socket.setblocking(False)

        # form image bytes
        img_byte_arr = sender2.form_image_bytes()

        # initialise stop and wait variables
        time_elapsed = 0            # time elapsed
        timeout_time = 0.02         # time before packet times out, 2xRTT=2x10ms=20ms
        seq_no = 0                  # packet sequence number
        counter = 0                 # counter to track packets sent
        begin_time = time.time()    # begininning time of initial transmission of file
        eof = False                 # end of file flag
        retransmissions = 0         # number of retransmissions
        send = True
        # while not received end of file flag
        while not eof:

            # initialise timeout to false
            timeout = False


            if send:
                # set self sequence number to the variable seq_no, in bytes
                self.sequenceNumber = seq_no.to_bytes(2, 'big')
                # send countherth packet with self.sequenceNumber
                sender2.send(client_socket, img_byte_arr[counter])
                # start timer
                t0 = time.time()
                send = False



            # initialise ack sequence number as None
            ack_seq_num = None

            if time.time() - t0 >= timeout_time:
                timeout = True

            try:
                ack_pack, server_address = client_socket.recvfrom(4000)
                ack_seq_num = ack_pack[0:2]
                ack_seq_num = int.from_bytes(ack_seq_num, "big")
            except error:
                pass

            # if timeout then do nothing and packet is resent on next loop
            if timeout:
                send = True
                # increment retransmissions
                retransmissions += 1
            else:
                # if incorrect ack sequence number then do nothing and packet is resent on next loop
                if ack_seq_num != seq_no:
                    # increment retransmissions
                    pass
                # otherwise the correct ack paket has been received
                else:
                    # increment sequence number
                    seq_no = increment_seq_no(seq_no)
                    # increment counter
                    counter += 1
                    send = True

            # check if EOF flag is 1, if so set eof True
            if self.EOF == (1).to_bytes(1, 'big'):
                eof = True

        # close client socket
        client_socket.close()
        # calculated elapsed time
        time_elapsed = time.time() - begin_time

        # print throughput: file size / time taken to send file
        print(retransmissions, round(self.fileSize / time_elapsed, 2))


if __name__ == "__main__":
    sender2 = Sender2()
    sender2.StopAndWait()
