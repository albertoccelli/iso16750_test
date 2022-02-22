#import pyvisa
from time import time, sleep
#import numpy as np
from gpib_alb import Instrument
from logs import log
from graph import Graph_IV


log_filename = "log.txt"
dat_filename = "test.dat"
graph_filename = "graph.png"


def ramp(start, stop, step):
    '''
    Generates a list of numbers according to a ramp
    
    Usage:
    >>> A = ramp(start, stop, step)
    '''
    decr = start > stop
    N = int(abs(stop-start)/step + 1)
    out = []
    for i in range(abs(N)):
        if decr:
            out.append(round((start - i*step), 3))
        else:
            out.append(round((start + i*step), 3))
    return out

# create the graphs
graph = Graph_IV()
graph.ylim2 = [15.9, 16]

generator = Instrument()

Us_min = 16
delay = 3 # wait time between steps (s)
U_steps = 0.025  # voltage steps (mV)
U = ramp(Us_min, 0, U_steps) + ramp(0, Us_min, U_steps)

input("-----------------------------------------------------\n"
      "Setup:\n"
      "Generator: %s" 
      "Ramp from %sV to 0 V, then back to %sV.\n"
      "- Delay: %ds\n"
      "- Step size: %0.3fV\n"
      "- Fall rate: %0.2fV/min\n"
      "- Estimated time: %02dh:%02dm:%02ds\n\n"
      "Press ENTER to begin...\n" % (generator.inst.query("*IDN?"), Us_min, Us_min, delay, U_steps, U_steps*(60/delay),(len(U)*delay)/3600,(len(U)*delay%3600)/60,(len(U)*delay%60)))
# start ramp
print("Setting up the generator...\n")
graph.print()
generator.operate()
start_time = time()
try:
    for i in range(len(U)):
        generator.set_volt(U[i])
        c = float(generator.get_curr())
        message = ("Volt: %0.3fV; \tCurr: %0.5fA; \tProg: %0.2f%%; \tT: %ds (ETA: %02dh:%02dm:%02ds)"
        % (U[i], c, 100*i/len(U), time()-start_time, ((len(U)-i)*delay)/3600,((len(U)-i)*delay%3600)/60, ((len(U)-i)*delay%60)))
        print(message)
        # print logs into .txt file
        log(log_filename, message)
        # print results in .dat file
        with open(dat_filename, "a") as o:
            if i == 0:
                o.write("Time(s)\tVoltage(V)\tCurrent(A)\n")
            o.write("%d\t%0.3f\t%0.5f\n" %(time()-start_time, U[i], c))
        # update current graph
        graph.update(time()-start_time, c, U[i])
        sleep(delay)
except KeyboardInterrupt:
    print("Interrupted.")
    graph.export(graph_filename)
    log(log_filename, "Test interrupted by user\n\n")
    generator.set_volt(0)
    quit()

graph.export(graph_filename)
log(log_filename, "END\n\n")
input("Test done! Congragulations")
