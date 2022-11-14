from CBD.Core import *
from CBD.lib.std import *
from CBD.lib.endpoints import SignalCollectorBlock
from CBD.simulator import *
from CBD.realtime.plotting import PlotManager, LinePlot, follow
from CBD.simulator import Simulator
import matplotlib.pyplot as plt


class CBDA(CBD):
    def __init__(self, name="CBDA"):
        CBD.__init__(self, name, input_ports=[""], output_ports=["OUT1"])

        # Create the blocks
        self.addBlock(TimeBlock("time"))
        self.addBlock(IntegratorBlock("integrator"))
        self.addBlock(ConstantBlock(block_name="ic", value=0))

        # Connect the blocks
        self.addConnection("time", "integrator")
        self.addConnection("ic", "integrator", input_port_name="IC")
        self.addConnection("integrator", "OUT1")

class CBDB(CBD):
    def __init__(self, name="CBDB"):
        CBD.__init__(self, name, input_ports=[""], output_ports=["OUT1"])

        # Create the blocks
        self.addBlock(TimeBlock("time"))
        self.addBlock(DerivatorBlock("integrator"))
        self.addBlock(ConstantBlock(block_name="ic", value=0))

        # Connect the blocks
        self.addConnection("time", "integrator")
        self.addConnection("ic", "integrator", input_port_name="IC")
        self.addConnection("integrator", "OUT1")

class SinGen(CBD):
    def __init__(self, name="SinGen"):
        CBD.__init__(self, name, input_ports=[], output_ports=["OUT1"])

        # Add the 't' parameter
        self.addBlock(TimeBlock("time"))
        self.addBlock(GenericBlock("sin", block_operator="sin"))

        # Connect them together
        self.addConnection("time", "sin", output_port_name='OUT1', input_port_name='IN1')
        self.addConnection("sin", "OUT1", output_port_name='OUT1')

class errorA(CBD):
    def __init__(self, CBDA, SIN,  name="ErrorA"):
        CBD.__init__(self, name, input_ports=[], output_ports=["OUT1"])
        # Sin
        # Add the 't' and "sin" parameter
        self.addBlock(CBDA)
        self.addBlock(SIN)

        # self.addBlock(TimeBlock("time"))
        self.addBlock(IntegratorBlock("integrator"))
        self.addBlock(ConstantBlock(block_name="ic", value=0))

        self.addBlock(AdderBlock(block_name="minus"))
        # self.addBlock(InverterBlock(block_name="inverted"))

        # Connect them together
        # self.addConnection("time", "integrator")
        self.addConnection("ic", "integrator", input_port_name="IC")

        self.addConnection("CBDA", "minus", input_port_name="IN1", output_port_name="OUT1")
        self.addConnection("SinGen", "minus", input_port_name="IN2", output_port_name="OUT1")

        self.addConnection("minus", "integrator", input_port_name="IN1", output_port_name="OUT1")
        self.addConnection("integrator", "OUT1")










        '''self.addConnection("time", "sin", output_port_name='OUT1', input_port_name='IN1')
        self.addConnection("ic", "integrator", input_port_name="IC")
        self.addConnection("sin", "OUT1", output_port_name='OUT1')

        self.addConnection("integrator", "OUT1")'''

def setUp(blockname):
    cbd = CBD(blockname)
    return cbd

def run(cbd, num_steps=1, delta_t=1.0):
    sim = Simulator(cbd)
    sim.setDeltaT(delta_t)
    sim.run(num_steps)

    data = cbd.getSignalHistory('OUT1')
    x, y = [x for x, _ in data], [y for _, y in data]
    return x, y

def simplePlot(x, y):
    plt.plot(x, y)
    plt.xlabel("Time")
    plt.ylabel("Value")
    plt.show()


if __name__ == '__main__':
    # CBDA
    cbda = CBDA()
    x, y = run(cbda, 10, 0.1)
    simplePlot(x, y)

    # CBDB
    cbdb = CBDB()
    x, y = run(cbdb, 10, 0.1)
    simplePlot(x, y)

    # Sin(t)
    sin = SinGen()
    x, y = run(sin, 10, 0.1)
    simplePlot(x, y)

    # ErrorA
    errorA_cbda = CBDA()
    errorA_singen = SinGen()
    errA = errorA(errorA_cbda, errorA_singen)
    x, y = run(errA, 10, 0.1)
    simplePlot(x, y)









