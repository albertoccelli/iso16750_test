from time import sleep, time
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

Us_min = 9


delay_1 = 5 # wait time when pulse is applied
delay_2 = 10 # wait time when V=U_smin
delay = delay_1+delay_2  # total wait time between steps

U_steps = 0.05*Us_min  # voltage steps (mV)

U = ramp(Us_min, 0, U_steps)

# create the graphs
graph = Graph_IV()
graph.ylim2 = [Us_min*0.99, Us_min*1.01]
generator = Instrument()



input("-----------------------------------------------------\n"
      "Setup:\n"
      "Generator: %s"
      "%sV for 10 seconds, alternating with a pulse with decreasing depth (5%% less each time) for 5 seconds, until 0 V is reached.\n"
      "- Delay: %ds\n"
      "- Step size: %0.3fV\n"
      "- Estimated time: %02dh:%02dm:%02ds\n\n"
      "Press ENTER to begin...\n" % (generator.inst.query("*IDN?"), Us_min, delay, U_steps, (len(U)*delay)/3600,(len(U)*delay%3600)/60,(len(U)*delay%60)))

# start pulse
print("Setting up the generator...\n")
graph.print()
generator.operate()
start_time = time()

try:
    generator.set_volt(Us_min)
    c = float(generator.get_curr())
    print("Voltage: %0.3fV" %Us_min)
    graph.update(time()-start_time, c, Us_min)
    sleep(delay_2)
    for i in range(1,len(U)):
        c = float(generator.get_curr())
        graph.update(time()-start_time, c, Us_min)
        generator.set_volt(U[i])
        c = float(generator.get_curr())
        message = ("Volt: %0.3fV; \tCurr: %0.5fA; \tProg: %0.2f%%; \tT: %ds (ETA: %02dh:%02dm:%02ds)"
        % (U[i], c, 100*i/len(U), time()-start_time, ((len(U)-i)*delay)/3600,((len(U)-i)*delay%3600)/60, ((len(U)-i)*delay%60)))
        print(message)
        log(log_filename, message)
        c = float(generator.get_curr())
        graph.update(time()-start_time, c, U[i])
        sleep(delay_1)
        c = float(generator.get_curr())
        graph.update(time()-start_time, c, U[i])
        generator.set_volt(Us_min)
        print("Voltage: %0.3fV" %Us_min)
        c = float(generator.get_curr())
        graph.update(time()-start_time, c, Us_min)
        sleep(delay_2)
except KeyboardInterrupt:
    generator.set_volt(0)
    print("Interrupted.")

graph.export(graph_filename)
log(log_filename, "END\n\n")
input("Test done! Congragulations")
    
