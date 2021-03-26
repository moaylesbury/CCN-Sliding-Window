from Sender1 import Sender
from socket import *
import time
import select

# extending Sender
def increment_seq_no(s):
    return 0 if s == 1 else 1


class Sender2(Sender):
    def __init__(self):
        super(Sender2, self).__init__()

    def ReceiveAck(self, client_socket, timeout_time):


        ready = select.select([client_socket], [], [], timeout_time)

        ack_pack = None
        print(ready)
        if ready[0]:
            ack_pack, server_address = client_socket.recvfrom(4000)


        if ack_pack is None:
            return None, True
        else:
            seq_num = ack_pack[0:2]
            return seq_num, False       # as timed out

    def StopAndWait(self):
        client_socket = socket(AF_INET, SOCK_DGRAM)

        img_byte_arr = sender2.form_image_bytes()

        time_elapsed = 0
        timeout_time = 0.02  # starting with 2xRTT=2x10ms=20ms

        seq_no = 0
        ack_seq_no = None
        counter = 0
        begin_time = time.time()
        eof = False
        retransmissions = 0

        while not eof:
            print("EOF: ", self.EOF)


            timeout = False

            print("=======================")
            print("COUNT:")
            print(counter)
            print("=======================")

            # send packet and start timer
            self.sequenceNumber = seq_no.to_bytes(2, 'big')

            print("packet sent")

            sender2.send(client_socket, img_byte_arr[counter])

            t0 = time.time()

            ack_seq_num = None
            # loop until an ack is received or timer times out
            while ack_seq_num is None and not timeout: # TODO: make this integrate better with RcvAck
                time_elapsed = time.time() - t0
                print("waiting")

                if time_elapsed >= timeout_time:
                    print("timeout")
                    timeout = True
                    break

                print("Time Elapsed: ", time_elapsed)

                ack_seq_num, timeout = sender2.ReceiveAck(client_socket, timeout_time)  # TODO: may need to catch socket error and return None



                print(ack_seq_num, timeout, time.time()-t0)
            print("timeout: ", timeout)
            # if timeout resent
            if timeout:
                print("+++++++++++++++++++++++")
                print("     retransmitted     ")
                print("+++++++++++++++++++++++")
                retransmissions += 1
                pass
            else:
                if ack_seq_num == 1:
                    print("+++++++++++++++++++++++")
                    print("     retransmitted     ")
                    print("+++++++++++++++++++++++")
                    retransmissions += 1
                    pass
                else:
                    time_elapsed = time.time() - t0  # successful, change seqno
                    seq_no = increment_seq_no(seq_no)
                    counter += 1

            if self.EOF == (1).to_bytes(1, 'big'):
                eof = True


        client_socket.close()
        print("final data")
        time_elapsed = time.time() - begin_time
        print(retransmissions, self.fileSize / time_elapsed)




if __name__ == "__main__":
    sender2 = Sender2()
    sender2.StopAndWait()
