import sys

from .bcolors import bcolors

def print_ok(msg):
    print(f"{msg} [{bcolors.OKGREEN}OK{bcolors.ENDC}]")

def print_fail(msg, console_output=""):
    print(f"{msg} [{bcolors.FAIL}FAIL{bcolors.ENDC}]\n{console_output}")

def print_unkown(msg):
    print(f"{msg} [{bcolors.WARNING}UNKNOWN{bcolors.ENDC}]")

# 0 - Service is OK.
# 1 - Service has a WARNING.
# 2 - Service is in a CRITICAL status.
# 3 - Service status is UNKNOWN.
def nagios_report(level, msg):
    match level:
        case "OK":
            print(f"OK - {msg}")
            sys.exit(0)
        case "WARNING":
            print(f"WARNING - {msg}")
            sys.exit(1)
        case "CRITICAL":
            print(f"CRITICAL - {msg}")
            sys.exit(2)
        case _:
            print(f"UNKNOWN - {msg}")
            sys.exit(3)