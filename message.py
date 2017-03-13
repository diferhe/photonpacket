from __future__ import print_function
import settings
from sys import stdout

def message(str, v):
    if v <= settings.verbose:
        print(str)

def progress(i):
    if settings.verbose == 0:
        pass
    elif settings.verbose == 1 and i % 100000 == 0:
        progressmessage(str(i/1000) + 'k')
    elif settings.verbose == 2 and i % 10000 == 0:
        progressmessage(str(i/1000) + 'k')
    elif settings.verbose == 3 and i % 1000 == 0:
        progressmessage(str(i/1000) + 'k')
    else:
        pass
    
def progressmessage(str):
    if settings.overwrite:
        stdout.write("\rprogress=%s" % str)
        stdout.flush()
    else:
        print(str)
        