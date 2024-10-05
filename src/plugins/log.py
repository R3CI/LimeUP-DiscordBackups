from src import *

def log(clr1, clr2, msg):
    print(f'{clr1}> {clr2}[{msg}]')

def dlog(status, resp):
    if DBG:
        print(f'{F.YELLOW}> {F.YELLOW}{status} {resp}')