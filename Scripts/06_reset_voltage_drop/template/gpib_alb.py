import pyvisa
from time import sleep

class Instrument:
    def __init__(self, name=None):
        self.inst = self.gpib_initialize(name)
        self.status = 0
        try:
            self.status = self.inst.query("OUTPUT?")
        except:
            pass
        
    def operate(self):
        """
        Enable the output
        """
        self.inst.write("OUTPUT ON")
        return
        
    def set_volt(self, value):
        """
        Set voltage value (in Volt)
        """
        val = str(value)
        self.inst.write("VOLT %s" % val)
        return

    def get_curr(self):
        """
        Read the current value (in Ampere)
        """
        return self.inst.query("MEAS:CURR?")

    def gpib_initialize(self, name=None):
        """
        Establish communication with GPIB instrument. If more than one instrument is
        available, then pick one from the list
        """
        rm = pyvisa.ResourceManager()
        instrument_list = rm.list_resources()
        if name is None:
            if len(instrument_list)>1:
                print("Available instruments (chose from the list below):\n")
                for i in range(len(instrument_list)):
                    print("%d) %s" %(i+1, instrument_list(i)))
                i_index = int(input("-->"))-1
                inst_str = instrument_list(i_index)
            else:
                inst_str = instrument_list[0]
        else:
            inst_str = name
            
        instrument = rm.open_resource(inst_str)        
        print("Current instrument: %s" %inst_str)

        return instrument      
