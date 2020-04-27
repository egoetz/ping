"""
CS330 Final Project

E Goetz, Aedan Pettit

Pinging with Python
----------------------------
This project is a command line tool that implements a Ping-like program
using python. The user may provide the program with a host name or ip address
as well as a port number, time interval or wait period.

The program will then send an ICMP Echo Request packet to the given address
and wait for a response. If a response is received before the program times out
then another packet will be sent. Ultimately, three packets are sent, and the
program displays the average, maximum, and minimum round trip times among
the packets sent as well as the number of packets sent, received, and dropped.

If port number is specified, then before initiating the ICMP protocol, the
program attempts to connect a socket to that particular port. If the connection
is successful then the port is open, if it is not then the port is closed. Even
if the port is closed ICMP packets can be sent and received because ICMP does
not use ports.
----------------------------
See Goetz for CLI structure and socket set up
See Pettit for Ping class and port checking
----------------------------
Acknowledgements to kyan001. "kyan001/ping3." GitHub, 11 Apr. 2020, github.com/kyan001/ping3.
"""


import sys, getopt, socket
from ping import Ping


def main(argv):
    """
    Ping a domain name or IP address. A specific port may be specified as well as the time interval to send pings at
    and the period of time to wait for responses.
    :param argv: The list of command line arguments and their corresponding values.
    :return: A number indicating the success or failure of the function call.
            0 = no issue
            1 = GetoptError
            2 = Specified both hostname and ip address
            3 = Invalid IPV4 number
            4 = Invalid IPV6 number
            5 = Invalid IP address of unrecognized type
            6 = Invalid port number
            7 = Non-numerical time interval
            8 = Non-numerical wait period
    """
    try:
        opts, args = getopt.getopt(argv, "hn:i:p:t:w:", ["host_name=", "ip_address=", "port=", "time_interval", "wait_period"])
    except getopt.GetoptError:
        sys.stderr.write('python3 main.py -n <host name> -i <ip address> -p <port number> -t <time interval> -w <wait period>\n')
        sys.exit(1)
    opt_specified = [opt for opt, arg in opts]
    time_interval_used = False
    wait_period_used = False
    port_requested = False
    if opt_specified.count('-h') != 0:
        print('python3 main.py -n <host name> -i <ip address> -p <port number> -t <time interval> -w <wait period>')
        sys.exit(0)
    elif opt_specified.count('-n') + opt_specified.count('-i') != 1:
        sys.stderr.write(
            'You specified more than one hostname, more than one IP address or a combination of hostnames and IP '
            'addresses. You specify one argument for -n or one argument for -i.\n')
        sys.exit(2)
    for opt, arg in opts:
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
                        sys.stderr.write(
                            'You specified an invalid IPV4 number. You must have four integers in the range [0, 255] '
                            'interspaced with the . character.\n')
                        sys.exit(3)
                addr = arg
            elif isinstance(arg, str) and arg.count(':') == 7:
                hexidecimals = arg.split(':')
                for hexidecimal in hexidecimals:
                    hexidecimal = int(hexidecimal, 16)
                    if not (hexidecimal >= 0 and hexidecimal <= 65535):
                        sys.stderr.write(
                            'You specified an invalid IPV6 number. You must have eight integers in the range [0, 65535]'
                            ' interspaced with the : character and written in hexadecimal.\n')
                        sys.exit(4)
                addr = arg
            else:
                sys.stderr.write('You specified an invalid IP address. You must use either IPV4 or IPV6 format.\n')
                sys.exit(5)
        if opt == '-p':
            port_requested = True
            if arg.isdigit() and (int(arg) >= 0  and int(arg) <= 65535):
                port = arg
            else:
                sys.stderr.write('You specified an invalid port number. You must choose an integer in [0, 65535].\n')
                sys.exit(6)
        if opt == '-t':
            if arg.isnumeric():
                time_interval = float(arg)
                time_interval_used = True
            else:
                sys.stderr.write('You specified an invalid time interval. You must choose an float.\n')
                sys.exit(7)
        if opt == '-w':
            if arg.isnumeric():
                wait_period = float(arg)
                wait_period_used = True
            else:
                sys.stderr.write('You specified an invalid time interval. You must choose an float.\n')
                sys.exit(8)

    if time_interval_used and wait_period_used:
        my_ping = Ping(addr, timeout=wait_period, time_between=time_interval, id=1)
    elif wait_period_used:
        my_ping = Ping(addr, timeout=wait_period, id=1)
    elif time_interval_used:
        my_ping = Ping(addr, time_between=time_interval, id=1)
    else:
        my_ping = Ping(addr, id = 1)
    if port_requested:
        port_open = False
        port_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        port_socket.settimeout(3)
        try:
            port_socket.connect((addr, int(port)))
            port_socket.shutdown(socket.SHUT_RDWR)
            port_open = True
        except:
            pass
        finally:
            port_socket.close()

        if port_open:
            print("Port number {} at {} is OPEN".format(port, addr))
        else:
            print("Port number {} at {} is CLOSED".format(port, addr))

    my_ping.run()

if __name__ == "__main__":
    main(sys.argv[1:])
