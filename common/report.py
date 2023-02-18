from .bcolors import bcolors

def print_ok(msg):
    print(f"{msg} [{bcolors.OKGREEN}OK{bcolors.ENDC}]")

def print_fail(msg, console_output=""):
    print(f"{msg} [{bcolors.FAIL}FAIL{bcolors.ENDC}]\n{console_output}")

def print_unkown(msg):
    print(f"{msg} [{bcolors.WARNING}UNKNOWN{bcolors.ENDC}]")