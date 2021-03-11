from Sender1 import Sender


# extending Sender
class Sender2(Sender):
    def __init__(self):
        pass

    def Send2(self):
        pass
        # send one packet
        # wait for ack
        # send next packet


if __name__ == "__main__":
    Sender2()