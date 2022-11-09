from CBD.Core import *
from CBD.lib.std import *
from CBD.lib.endpoints import SignalCollectorBlock
from CBD.Core import CBD
from CBD.simulator import Simulator

class SinGen(CBD):
    def __init__(self, name="SinGen"):
        CBD.__init__(self, name, input_ports=[], output_ports=[])

        # Create the blocks
        self.addBlock(TimeBlock("time"))
        self.addBlock(IntegratorBlock("cbda"))
        #self.addBlock(GenericBlock("sin", block_operator="sin"))
        #self.addBlock(SignalCollectorBlock("collector"))

        # Connect the blocks
        self.addConnection("time", "cbda")
        #self.addConnection("cbda", "collector")


model = SinGen()
sim = Simulator(model)
sim.run(10.0)
