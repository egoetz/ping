import sys, getopt, socket
from ping import Ping

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hn:i:p:t:w:", ["host_name=", "ip_address=", "port=", "time_interval", "wait_period"])
    except getopt.GetoptError:
        print('test.py -n <host name> -i <ip address> -p <port number> -t <time interval> -w <wait period>')
        sys.exit(2)
    opt_specified = [opt for opt, arg in opts]
    if opt_specified.count('-n') + opt_specified.count('-i') != 1:
        raise ValueError(
            'You specified more than one hostname, more than one IP address or a combination of hostnames and IP '
            'addresses. You specify one argument for -n or one argument for -i.')
    for opt, arg in opts:
        if opt == '-h':
            print('test.py -n <host name> -i <ip address> -p <port number> -t <time interval> -w <wait period>')
            sys.exit()
        if opt == '-n':
            # Want to get the ip address from the hostname
            _, _, _, _, addr = socket.getaddrinfo(arg, 0)[0]
            # addr is a (host, port) tuple and we don't need the port for ICMP
            addr = addr[0]
        if opt == '-i':
            if isinstance(arg, str) and arg.count('.') == 3:
                byte_list = arg.split('.')
                for byte in byte_list:
                    byte = int(byte)
                    if not (byte >= 0 and byte <= 255):
                        raise ValueError(
                            'You specified an invalid IPV4 number. You must have four integers in the range [0, 255] '
                            'interspaced with the . character.')
                addr = arg
            elif isinstance(arg, str) and arg.count(':') == 7:
                hexidecimals = arg.split(':')
                for hexidecimal in hexidecimals:
                    hexidecimal = int(hexidecimal, 16)
                    if not (hexidecimal >= 0 and hexidecimal <= 65535):
                        raise ValueError(
                            'You specified an invalid IPV6 number. You must have eight integers in the range [0, 65535]'
                            ' interspaced with the : character and written in hexadecimal.')
                addr = arg
            else:
                raise ValueError('You specified an invalid IP address. You must use either IPV4 or IPV6 format.')
                sys.exit()
        if opt == '-p':
            if arg.isdigit() and (int(arg) >= 0  and int(arg) <= 65535):
                port = arg
            else:
                raise ValueError('You specified an invalid port number. You must choose an integer in [0, 65535].')
                sys.exit()
        if opt == 't':
            if isinstance(arg, float):
                time_interval = arg
            else:
                raise ValueError('You specified an invalid time interval. You must choose an float.')
        if opt == 'w':
            if isinstance(arg, float):
                wait_period = arg
            else:
                raise ValueError('You specified an invalid time interval. You must choose an float.')

    my_ping = Ping(addr, id = 1)
    my_ping.run()



# Options of potential use:
# Timing
# SIOCGSTAMP - Return a struct timeval with the receive timestamp of the last packet passed to the user.
# SO_TIMESTAMP - cmsg_data field is a struct timeval indicating the reception time of the last packet passed to the user in this call.
# Info on IP Address capabilities
# SO_PEERCRED - Return the credentials of the foreign process connected to this socket.
# SO_ACCEPTCONN - Returns a value indicating whether or not this socket has been marked to accept connections with listen(2)
# Change sending method:
# SO_MARK - Set the mark for each packet sent through this socket (similar to the netfilter MARK target but socket-based). Changing the mark can be used for mark-based routing without netfilter or for packet filtering.
# SO_KEEPALIVE -     Enable sending of keep-alive messages on connection-oriented sockets. Expects an integer boolean flag.
# SO_DONTROUTE - Don't send via a gateway, send only to directly connected hosts.
# SO_DEBUG - enable socket debug
# SO_BSDCOMPAT - Enable BSD bug-to-bug compatibility. If enabled, ICMP errors received for a UDP socket will not be passed to the user program.
# SO_BROADCAST - Set or get the broadcast flag. When enabled, datagram sockets are allowed to send packets to a broadcast address.

if __name__ == "__main__":
    main(sys.argv[1:])
