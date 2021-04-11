import sys
import re

from ping import BRP5088_ping
from traceroute import BRP5088_traceroute


# Desc: This project implements the linux commands ping and traceroute.
# Author: Brett Patterson
# Date: 4/11/2021



ping_traceRoute_regex = "(BRP5088_ping|BRP5088_traceroute)"


def main():
    inputString = input( "BRP5088_ping or BRP5088_traceroute:" )
    
    inputString = "BRP5088_ping google.com -c 32 -i 10 -s 57 -t 45" # ping

    # figures if the user wants to use ping or traceroute
    result = re.search( ping_traceRoute_regex, inputString )

    if result == None:
        print("\033[1;31;40mYou didn't enter a valid program command.",
              "\033[1;34;40mYour options are: \033[1;32;40mBRP5088_ping \033[1;34;40mor \033[1;32;40mBRP5088_traceroute\033[1;37;40m" )
    else:
        
        if result.group() == "BRP5088_ping":
            BRP5088_ping( inputString )
        else:
            BRP5088_traceroute( inputString ) 


if __name__ == "__main__":
    main()
