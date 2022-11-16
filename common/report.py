from .bcolors import bcolors

def print_ok(msg):
    print(f"{msg} [{bcolors.OKGREEN}OK{bcolors.ENDC}]\n")

def print_fail(msg, result=""):
    print(f"{msg} [{bcolors.FAIL}FAIL{bcolors.ENDC}]\n{result}\n")

def print_unkown(msg):
    print(f"{node_instance} [{bcolors.WARNING}UNKNOWN{bcolors.ENDC}]")