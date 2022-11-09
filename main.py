from CBD.Core import *
from CBD.lib.std import TimeBlock, GenericBlock, IntegratorBlock, DerivatorBlock
from CBD.lib.endpoints import SignalCollectorBlock
from CBD.simulator import *
from CBD.realtime.plotting import PlotManager, LinePlot, follow
from CBD.simulator import Simulator
import matplotlib.pyplot as plt


class CBDA(CBD):
    def __init__(self, name="CBDA"):
        CBD.__init__(self, name, input_ports=[""], output_ports=["Xa"])

        # Create the blocks
        self.addBlock(TimeBlock("time"))
        self.addBlock(IntegratorBlock("integrator"))
        self.addBlock(ConstantBlock(block_name="ic", value=0))

        # Connect the blocks
        self.addConnection("time", "integrator")
        self.addConnection("ic", "integrator", input_port_name="IC")
        self.addConnection("integrator", "Xa")

class CBDB(CBD):
    def __init__(self, name="CBDA"):
        CBD.__init__(self, name, input_ports=[""], output_ports=["Xa"])

        # Create the blocks
        self.addBlock(TimeBlock("time"))
        self.addBlock(DerivatorBlock("integrator"))
        self.addBlock(ConstantBlock(block_name="ic", value=0))

        # Connect the blocks
        self.addConnection("time", "integrator")
        self.addConnection("ic", "integrator", input_port_name="IC")
        self.addConnection("integrator", "Xa")

class SinGen(CBD):
    def __init__(self, name="SinGen"):
        CBD.__init__(self, name, input_ports=[], output_ports=["OUT1"])

        # Add the 't' parameter
        # Let's call it 'time'
        self.addBlock(TimeBlock("time"))

        # Add the block that computes the actual sine function
        # Let's call it 'sin'
        self.addBlock(GenericBlock("sin", block_operator="sin"))

        # Connect them together
        self.addConnection("time", "sin", output_port_name='OUT1',
                                            input_port_name='IN1')

        # Connect the output port
        self.addConnection("sin", "OUT1", output_port_name='OUT1')


if __name__ == '__main__':
    cbda = SinGen("CBDA")

    sim = Simulator(cbda)
    sim.setDeltaT(0.1)
    sim.run(10)

    data = cbda.getSignalHistory('OUT1')
    x, y = [x for x, _ in data], [y for _, y in data]

    print(x)
    print(y)
    plt.plot(x, y)
    plt.xlabel("Time")
    plt.ylabel("Value")
    plt.show()









