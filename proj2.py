import sys
import re

import ping
import traceroute

ping_traceRoute_regex = "(BRP5088_ping|BRP5088_traceroute)"


def main():
    answer = input( "BRP5088_ping or BRP5088_traceroute:" )

    # figures if the user wants to use ping or traceroute
    result = re.search( ping_traceRoute_regex, answer )

    print( f"result= { result }" )

    print( f"type == { type( result )}")

    if result == None:
        print("\033[1;31;40mYou didn't enter a valid program command.",
              "\033[1;34;40mYour options are: \033[1;32;40mBRP5088_ping \033[1;34;40mor \033[1;32;40mBRP5088_traceroute\033[1;37;40m")


if __name__ == "__main__":
    main()
