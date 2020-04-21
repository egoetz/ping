import os, math, struct, socket
from timeit import default_timer as timer

# From RFC792
ICMP_ECHO_REQUEST = 8
ICMP_ECHO_REPLY = 0
ICMP_MAX_RECV = 2048


# credit to https://www.binarytides.com/raw-socket-programming-in-python-linux/
def internet_checksum(msg):
	s = 0

	# loop taking 2 characters at a time
	for i in range(0, len(msg), 2):
		w = ord(msg[i]) + (ord(msg[i+1]) << 8 )
		s = s + w

	s = (s >> 16) + (s & 0xffff)
	s = s + (s >> 16)

	#complement and mask to 4 byte short
	s = ~s & 0xffff

	return s


class Ping():
    """
    This class handles information related to the ping request
    It stores the destination of the ping as well as other relavent information
    """
    def __init__(self, destination, timeout=1000, packet_size=55, id=None):
        self.destination = destination
        self.timeout = timeout
        self.packet_size = packet_size
        self.id = id
        self.sequence_number = 0
        self.sent = 0
        self.recieved = 0
        self.min_time = math.inf
        self.max_time = 0
        self.total_time = 0

        if self.id is None:
            self.id = os.getpid()


    def run(self, count, timeout):
        """
        Continually sends and receives ping messages until count or timeout is reached
        """
        pass

    def send(self, sock):
        """
        Sends a single ping using the socket sock
        """
        checksum = 0

        header = struct.pack(
            "!BBHHH", ICMP_ECHO_REQUEST, 0, checksum, self.id, self.sequence_number
        )

        padBytes = []
        startVal = 0x42
        for i in range(startVal, startVal + (self.packet_size)):
            padBytes += [(i & 0xff)]

        data = bytes(padBytes)
        checksum = internet_checksum(data)

        header = struct.pack(
            "!BBHHH", ICMP_ECHO_REQUEST, 0, checksum, self.id, self.sequence_number
        )

        packet = header + data
        sent_time = timer()

        try:
            sock.sendto(packet, (self.destination, 1))
        except socket.error as e:
            print("Ping failed with error: {}".format(e))
            sock.close()
            return

        return sent_time


    def receive(self):
        """
        Receives a single ping
        """
        pass

# Used for testing only
if __name__ == "__main__":
    current_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname("icmp"))
    current_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    myPing = Ping("127.0.0.1")
    myPing.send(current_socket)
