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
        self.addBlock(DerivatorBlock("derivator"))
        self.addBlock(ConstantBlock(block_name="ic", value=0))

        # Connect the blocks
        self.addConnection("time", "derivator")
        self.addConnection("ic", "derivator", input_port_name="IC")
        self.addConnection("derivator", "OUT1")

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
    def __init__(self,  name="ErrorA"):
        CBD.__init__(self, name, input_ports=[], output_ports=["OUT1"])
        errorA_cbda = CBDA()
        errorA_sin = SinGen()

        # Add all blocks
        self.addBlock(errorA_cbda)
        self.addBlock(errorA_sin)
        self.addBlock(IntegratorBlock("integrator"))
        self.addBlock(ConstantBlock(block_name="ic", value=0))
        self.addBlock(AdderBlock(block_name="minus"))
        self.addBlock(NegatorBlock(block_name="negator"))
        self.addBlock(AbsBlock(block_name="absolute"))

        # Connect them together
        self.addConnection("ic", "integrator", input_port_name="IC")
        self.addConnection("CBDA", "negator", input_port_name="IN1", output_port_name="OUT1")
        self.addConnection("SinGen", "minus", input_port_name="IN1", output_port_name="OUT1")
        self.addConnection("negator", "minus", input_port_name="IN2", output_port_name="OUT1")
        self.addConnection("minus", "absolute", input_port_name="IN1", output_port_name="OUT1")
        self.addConnection("absolute", "integrator", input_port_name="IN1", output_port_name="OUT1")
        self.addConnection("integrator", "OUT1")

class errorB(CBD):
    def __init__(self,  name="ErrorA"):
        CBD.__init__(self, name, input_ports=[], output_ports=["OUT1"])
        errorB_cbdb = CBDB()
        errorB_sin = SinGen()

        # Add all blocks
        self.addBlock(errorB_cbdb)
        self.addBlock(errorB_sin)
        self.addBlock(IntegratorBlock("integrator"))
        self.addBlock(ConstantBlock(block_name="ic", value=0))
        self.addBlock(AdderBlock(block_name="minus"))
        self.addBlock(NegatorBlock(block_name="negator"))
        self.addBlock(AbsBlock(block_name="absolute"))

        # Connect them together
        self.addConnection("ic", "integrator", input_port_name="IC")
        self.addConnection("CBDB", "negator", input_port_name="IN1", output_port_name="OUT1")
        self.addConnection("SinGen", "minus", input_port_name="IN1", output_port_name="OUT1")
        self.addConnection("negator", "minus", input_port_name="IN2", output_port_name="OUT1")
        self.addConnection("minus", "absolute", input_port_name="IN1", output_port_name="OUT1")
        self.addConnection("absolute", "integrator", input_port_name="IN1", output_port_name="OUT1")
        self.addConnection("integrator", "OUT1")

def setUp(blockname):
    cbd = CBD(blockname)
    return cbd

def run(cbd, num_steps, delta_t):
    sim = Simulator(cbd)
    print(delta_t)
    sim.setDeltaT(delta_t)
    sim.run(num_steps)

    data = cbd.getSignalHistory('OUT1')
    x, y = [x for x, _ in data], [y for _, y in data]
    return x, y

def simplePlot(x, y, title):
    plt.plot(x, y)
    plt.xlabel("Time")
    plt.ylabel("Value")
    plt.title(title)
    plt.show()


if __name__ == '__main__':
    # CBDA
    cbda = CBDA()
    #delta=0.001
    #x, y = run(cbda, 10, delta)
    #simplePlot(x, y, f"CBDA, delta={delta}")

    # CBDB
    cbdb = CBDB()
    #delta = 0.1
    #x, y = run(cbdb, 10, delta)
    #simplePlot(x, y, f"CBDB, delta={delta}")

    # Sin(t)
    sin = SinGen()
    delta = 0.001
    x, y = run(sin, 10, delta)
    simplePlot(x, y, f"SIN, delta={delta}")

    # ErrorA
    #errA = errorA()
    #x, y = run(errA, 50, 0.001)
    #simplePlot(x, y, "ErrorA")

    # ErrorB
    #errB = errorB()
    #x, y = run(errB, 50, 0.1)
    #simplePlot(x, y, "ErrorB")









