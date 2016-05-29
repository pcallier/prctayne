#!/usr/bin/env python
"""
super.py

Interface with supercollider using processes.
Will dispatch supercollider code to an sclang
process (which itself starts and dispatches to an scsynth
server process)
"""

import time
import subprocess
from multiprocessing import Process, Pipe

def sclang():
    """ Start sclang and boot the SC3 server
    
    Returns the sclang process object
    """

    sclg = subprocess.Popen(['sclang'], 
            stdin = subprocess.PIPE,
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE)
    print >> sclg.stdin, "s.boot;"

#    while True:
#        x = wait_for_output(sclg.stdout)
#        if x is None:
#            break
#        print x
#
    time.sleep(2.0)

    return sclg

def send_sine(sclg):
    cmd = "{ x=SinOsc.ar(rrand(220,550)); y=EnvGen.ar(Env.linen(0.01, 0.2, 0.25, 1.0));" \
    "FreeSelfWhenDone.kr(y); x*y }.play;"

    print cmd
    print >> sclg.stdin, cmd

def shutdown(sclg):
    print >> sclg.stdin, "s.quit; \n\004"
    stdout, stderr = sclg.communicate()
    return stdout, stderr

def wait_for_output(stream, timeout=3.0):
    """ Poll a stream for output for a certain time before giving up """
    pipe_1, pipe_2 = Pipe()
    p = Process(target = poll_iterable, args = (stream, pipe_2))
    p.start()
    p.join(timeout)
    p.terminate()
    if pipe_1.poll():
        return pipe_1.recv()
    else:
        return None

def poll_iterable(stream, pipe):
    pipe.send(stream.next())
    pipe.close()

def main():
    sclg = sclang()
    send_sine(sclg)
    send_sine(sclg)
    time.sleep(5.0)
    out, err = shutdown(sclg)
    print out

if __name__=="__main__":
    main()
