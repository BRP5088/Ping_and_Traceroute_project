import sys

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


def BRP5088_ping():
    return None
