import sys
import re


# Desc: We use ping to check network connectivity and to see whether a remote server is up and running. 
#       Ping sends an ICMP echo request packet to the server which will in turn reply an ICMP echo reply packet to the sender.





# This represents the address the user would like to ping
address = None

# Stop after sending (and receiving) count ECHO_RESPONSE packets. If this option is not specified, ping will operate until interrupted.
# -c count
count = None

# Wait wait seconds between sending each packet. The default is to wait for one second between each packet.
# -i wait
waitTime = 1

# Specify the number of data bytes to be sent. The default is 56, which translates into 64 ICMP data bytes when combined with the 8 bytes of ICMP header data.
# -s packetsize
packetByteSize = 56

# Specify a timeout, in seconds, before ping exits regardless of how many packets have been received.
# -t timeout
timeoutPeriod = None


initializer_regex = "(\-c|\-i|\-s|\-t) (\d+)"
address_regex = "([a-zA-Z]+\.[a-zA-Z]+|\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"


def initialize_ping( inputString ):
    matches = re.findall( initializer_regex, inputString )
    for match in matches:
        if match[0] == "-c":
            count = int( match[1] )
            continue
        
        if match[0] == "-i":
            waitTime = int( match[1] )
            continue

        if match[0] == "-s":
            packetByteSize = int( match[1] )
            continue

        if match[0] == "-t":
            timeoutPeriod = int( match[1] )
            continue
    
    matches = re.findall( address_regex, inputString )

    if len( matches ) == 0:
        print("\033[1;31;40mForgot the destination address for the ping!\033[1;37;40m")
        sys.exit( 1234 )
    
    if len( matches ) > 1:
        print( "\033[1;31;40mPut too many address in the ping command!\033[1;37;40m")
        sys.exit(1234)

    address = matches[ 0 ]

    print( address )
    

def BRP5088_ping( inputString ):
    initialize_ping( inputString )

    """
        bepatt@Snoopy:~$ ping 172.217.165.142
        PING 172.217.165.142 (172.217.165.142) 56(84) bytes of data.
        64 bytes from 172.217.165.142: icmp_seq=1 ttl=116 time=10.5 ms
        64 bytes from 172.217.165.142: icmp_seq=2 ttl=116 time=19.7 ms
        64 bytes from 172.217.165.142: icmp_seq=3 ttl=116 time=12.8 ms
        64 bytes from 172.217.165.142: icmp_seq=4 ttl=116 time=11.4 ms
        64 bytes from 172.217.165.142: icmp_seq=5 ttl=116 time=13.9 ms
        64 bytes from 172.217.165.142: icmp_seq=6 ttl=116 time=18.6 ms
        64 bytes from 172.217.165.142: icmp_seq=7 ttl=116 time=13.0 ms
        64 bytes from 172.217.165.142: icmp_seq=8 ttl=116 time=15.8 ms
        64 bytes from 172.217.165.142: icmp_seq=9 ttl=116 time=12.2 ms
        64 bytes from 172.217.165.142: icmp_seq=10 ttl=116 time=13.4 ms
        64 bytes from 172.217.165.142: icmp_seq=11 ttl=116 time=13.5 ms
        64 bytes from 172.217.165.142: icmp_seq=12 ttl=116 time=16.6 ms
        ^C
        --- 172.217.165.142 ping statistics ---
        12 packets transmitted, 12 received, 0% packet loss, time 11010ms
        rtt min/avg/max/mdev = 10.551/14.337/19.757/2.714 ms
        """






    return None
