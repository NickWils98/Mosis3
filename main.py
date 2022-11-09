'''from CBD.Core import *
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

        # Connect the blocks
        self.addConnection("time", "integrator")
        self.addConnection("integrator", "Xa")

if __name__ == '__main__':
    cbda = CBDA("cbda")

    sim = Simulator(cbda)
    sim.run(10.0)


'''

from CBD.Core import *   # To prevent circular dependency
from CBD.lib.std import TimeBlock, GenericBlock

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


sinGen = SinGen("SinGen")

from CBD.simulator import Simulator

sim = Simulator(sinGen)

manager = PlotManager()
manager.register("sin", sinGen.find('collector')[0], (fig, ax), LinePlot(color='red'))
manager.connect('sin', 'update', lambda d, axis=ax: axis.set_xlim(follow(d[0], 10.0, lower_bound=0.0)))

# The termination time can be set as argument to the run call
sim.run(20.0)

data = sinGen.getSignalHistory('OUT1')
x, y = [x for x, _ in data], [y for _, y in data]

print(x)
print(y)