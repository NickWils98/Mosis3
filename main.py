from CBD.Core import *
from CBD.lib.std import TimeBlock, GenericBlock, IntegratorBlock, DerivatorBlock
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
    def __init__(self, name="CBDA"):
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
    def __init__(self, param1, param2,  name="CBDA"):
        CBD.__init__(self, name, input_ports=["sinT", "Xa"], output_ports=["OUT1"])

        # Create the blocks
        self.addBlock(TimeBlock("time"))
        self.addBlock(DerivatorBlock("integrator"))
        #self.addBlock(ConstantBlock(block_name="ic", value=0))

        # Connect the blocks
        self.addConnection("sinT", "integrator")
        self.addConnection("ic", "integrator")
        self.addConnection("integrator", "OUT1")

def setUp(blockname):
    cbd = CBD(blockname)
    return cbd

def run(cbd, num_steps=1, delta_t=1.0, ):
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
    cbda = CBDA("CBDA")
    x, y = run(cbda, 10, 0.1)
    simplePlot(x, y)

    # CBDB
    cbdb = CBDB("CBDA")
    x, y = run(cbdb, 10, 0.1)
    simplePlot(x, y)

    # Sin(t)
    sin = SinGen("SIN")
    x, y = run(sin, 10, 0.1)
    simplePlot(x, y)









