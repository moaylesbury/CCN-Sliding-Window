from Sender1 import Sender
from socket import *
import time

# extending Sender
def increment_seq_no(s):
    return 0 if s == 1 else 1


class Sender2(Sender):
    def __init__(self):
        super(Sender2, self).__init__()

    def ReceiveAck(self, client_socket):
        ack_pack, server_address = client_socket.recvfrom(4000)
        seq_num = ack_pack[0:2]
        return seq_num

    def StopAndWait(self):
        client_socket = socket(AF_INET, SOCK_DGRAM)
        img_byte_arr = Sender.form_image_bytes(self)
        time_elapsed = 0
        timeout_time = 0.02  # starting with 2xRTT=2x10ms=20ms
        seq_no = 0

        while not self.EOF:
            opposite_state = 0
            timeout = False

            while not self.EOF:

                # send packet and start timer
                sender2.Sender.send(client_socket, img_byte_arr[seq_no])
                t0 = time.time()

                # loop until an ack is received or timer times out
                while seq_num is None and time.time() - t0 < timeout_time:
                    seq_num = sender2.ReceiveAck(client_socket)  # may need to catch socket error and return None

                    if time.time() - t0 >= timeout_time:
                        timeout = True

                # if timeout resent
                if timeout:
                    pass
                else:
                    if seq_num == 1:
                        pass
                    else:
                        time_elapsed = time.time() - t0 #successful, change seqno
                        seq_no = increment_seq_no(seq_no)





if __name__ == "__main__":
    sender2 = Sender2()
    sender2.StopAndWait()
