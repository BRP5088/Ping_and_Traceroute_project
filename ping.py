import sys
import re
import socket

import time
import random

import struct
import os

# Desc: We use ping to check network connectivity and to see whether a remote server is up and running. 
#       Ping sends an ICMP echo request packet to the server which will in turn reply an ICMP echo reply packet to the sender.












initializer_regex = "(\-c|\-i|\-s|\-t) (\d+)"
address_regex = "([a-zA-Z]+\.[a-zA-Z]+(?:\.[a-zA-Z]+)?|\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"


# ICMP parameters
ICMP_ECHOREPLY = 0  # Echo reply (per RFC792)
ICMP_ECHO = 8  # Echo request (per RFC792)
ICMP_MAX_RECV = 2048  # Max size of incoming buffer


class Ping:

    def __init__(self, inputString ):
        # This represents the address the user would like to ping
        self.address = None

        # Stop after sending (and receiving) count ECHO_RESPONSE packets. If this option is not specified, ping will operate until interrupted.
        # -c count
        self.count = -1

        # Wait wait seconds between sending each packet. The default is to wait for one second between each packet.
        # -i wait
        waitTime = 1

        # Specify the number of data bytes to be sent. The default is 56, which translates into 64 ICMP data bytes when combined with the 8 bytes of ICMP header data.
        # -s packetsize
        packetByteSize = 56

        # Specify a timeout, in seconds, before ping exits regardless of how many packets have been received.
        # -t timeout
        timeoutPeriod = 2

        self.initialize_ping( inputString )

        self.own_id = os.getpid()

        self.seq_number = 0

        self.completedPings = 0

        self.total_time = 0

        self.min_time = -1

        self.max_time = sys.maxsize

        self.response = None

        self.quiet_output = None

        




    def initialize_ping(self, inputString ):
        matches = re.findall( initializer_regex, inputString )
        for match in matches:
            if match[0] == "-c":
                self.count = int(match[1])
                continue
            
            if match[0] == "-i":
                self.waitTime = int( match[1] )
                continue

            if match[0] == "-s":
                self.packetByteSize = int( match[1] )
                continue

            if match[0] == "-t":
                self.timeoutPeriod = int( match[1] )
                continue
        
        matches = re.findall( address_regex, inputString )

        if len( matches ) == 0:
            print("\033[1;31;40mForgot the destination address for the ping!\033[1;37;40m")
            sys.exit( 1234 )
        
        if len( matches ) > 1:
            print( "\033[1;31;40mPut too many address in the ping command!\033[1;37;40m")
            sys.exit(1234)

        self.address = matches[ 0 ]

    
    def run(self):

        interation = 0

        while True:

            print(f"interation= { interation }")



            delay = self.complete_single_ping_interation()
            self.seq_number += 1




            interation += 1
            if interation >= self.count:
                break

        print("exited")


    def print_success(self, delay, ip, packet_size, ip_header, icmp_header):
        if ip == self.address:
                from_info = ip
        else:
            from_info = "%s (%s)" % (self.address, ip)

            msg = "%d bytes from %s: icmp_seq=%d ttl=%d time=%.1f ms" % (
                packet_size, from_info, icmp_header["seq_number"], ip_header["ttl"], delay)

            if self.quiet_output:
                self.response.output.append(msg)
                self.response.ret_code = 0
            else:
                print(msg)
            #print("IP header: %r" % ip_header)
            #print("ICMP header: %r" % icmp_header)



    def complete_single_ping_interation( self ):

        current_socket = socket.socket( socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname("icmp") )


        send_time = self.send_a_ping( current_socket )


        self.send_count += 1

        receive_time, packet_size, ip, ip_header, icmp_header = self.receive_a_ping( current_socket )
        current_socket.close()


        if receive_time:
            self.completedPings += 1

            delay = (receive_time - send_time) * 1000.0
            self.total_time += delay

            if self.min_time > delay:
                self.min_time = delay
			
            if self.max_time < delay:
                self.max_time = delay

            self.print_success(delay, ip, packet_size, ip_header, icmp_header)
            return delay


        else:
            print( "failed to get a response" )



        return None




    def calculate_checksum(self, source_string):
        """
        I'm not too confident that this is right but testing seems
        to suggest that it gives the same answers as in_cksum in ping.c
        """

        sum = 0
        countTo = (len(source_string)/2)*2
        count = 0
        while count < countTo:
            print(source_string )

            tmp = ord( source_string[count + 1])*256+ord(source_string[count] )
            print( f"thing = { tmp }" )

            print(ord(source_string[count + 1]) *
                  256 + ord(source_string[count] ) )


            sys.exit(432)

            thisVal = ord(source_string[count + 1])*256 + ord(source_string[count])
            sum = sum + thisVal
            sum = sum & 0xffffffff  # Necessary?
            count = count + 2

        if countTo < len(source_string):
            

            sum = sum + ord(source_string[len(source_string) - 1])
            sum = sum & 0xffffffff  # Necessary?

        sum = (sum >> 16) + (sum & 0xffff)
        sum = sum + (sum >> 16)
        answer = ~sum
        answer = answer & 0xffff

        # Swap bytes. Bugger me if I know why.
        answer = answer >> 8 | (answer << 8 & 0xff00)

        return answer



    def send_a_ping( self, current_socket ):
        # Header is type (8bits), code (8bits), checksum (16bits), id (16bits), sequence (16bits)
        
        checksum = 0
        header = struct.pack( "!BBHHH", ICMP_ECHO, 0, checksum, self.own_id, self.seq_number ) # THis is a dummy header


        padBytes = []
        startVal = 0x42
        for i in range(startVal, startVal + self.packetByteSize ):
            padBytes += [(i & 0xff)]  # Keep chars in the 0-255 range
        data = bytes(padBytes)

        # Calculate the checksum on the data and the dummy header.
        checksum = self.calculate_checksum(header + data) # Checksum is in network order

        sys.exit( 123 )


        # Now that we have the right checksum, we put that in. It's just easier
        # to make up a new header than to stuff it into the dummy.
        header = struct.pack( "!BBHHH", ICMP_ECHO, 0, checksum, self.own_id, self.seq_number )

        packet = header + data

        send_time = default_timer()

        try:
            current_socket.sendto(packet, (self.address, 1)) # Port number is irrelevant for ICMP
        except socket.error as e:
            self.response.output.append("General failure (%s)" % (e.args[1]))
            current_socket.close()
            return

        return send_time

    def receive_a_ping( self ):
        
        timoout = self.waitTime
        
        
        
        return None












def BRP5088_ping( inputString ):

    p = Ping( inputString )

    p.run()


    # initialize_ping( inputString )
    # send_pings( address, count, timeoutPeriod )



    # print( f"after init Address is: { address }" )
    # print( f"Hostname: { socket.gethostbyname( address ) }" )

    
    
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




        PING www.google.com (172.217.12.132) 56(84) bytes of data.
        64 bytes from lga34s19-in-f4.1e100.net (172.217.12.132): icmp_seq=1 ttl=115 time=20.6 ms
        64 bytes from lga34s19-in-f4.1e100.net (172.217.12.132): icmp_seq=2 ttl=115 time=23.4 ms
        64 bytes from lga34s19-in-f4.1e100.net (172.217.12.132): icmp_seq=3 ttl=115 time=21.6 ms
        64 bytes from lga34s19-in-f4.1e100.net (172.217.12.132): icmp_seq=4 ttl=115 time=23.6 ms
        ^C
        --- www.google.com ping statistics ---
        4 packets transmitted, 4 received, 0% packet loss, time 3003ms
        rtt min/avg/max/mdev = 20.690/22.351/23.619/1.238 ms




        """






    return None
