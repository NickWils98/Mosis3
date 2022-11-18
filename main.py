from CBD.Core import *
from CBD.lib.std import *
from CBD.lib.endpoints import SignalCollectorBlock
from CBD.simulator import *
from CBD.realtime.plotting import PlotManager, LinePlot, follow
from CBD.simulator import Simulator
import matplotlib.pyplot as plt
# Import the latexify core unit
from CBD.converters.latexify import CBD2Latex
from CBD.preprocessing.butcher import ButcherTableau as BT
from CBD.preprocessing.rungekutta import RKPreprocessor
# OR, ALTERNATIVELY
from CBD.converters.latexify.CBD2Latex import CBD2Latex


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
        self.addConnection("time", "sin", input_port_name='IN1', output_port_name='OUT1')
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

def checkValitidyLatex(model):
    cbd2latex = CBD2Latex(model, show_steps=True, render_latex=False)

    cbd2latex.simplify()

    # print the resulting equations
    print("RESULT IS:")
    print(cbd2latex.render())

def transformToRKF(model, delta_t, start_time, atol, hmin, safety):
    model.addFixedRateClock("clock", delta_t=delta_t, start_time=start_time)

    tableau = BT.RKF45()
    RKP = RKPreprocessor(tableau, atol=atol, hmin=hmin, safety=safety)
    new_model = RKP.preprocess(model)

    return new_model

def run(cbd, num_steps, delta_t, title, RKF=False):
    sim = Simulator(cbd)
    if RKF==False:
        sim.setDeltaT(delta_t)
    sim.run(num_steps)

    data = cbd.getSignalHistory('OUT1')
    x, y = [x for x, _ in data], [y for _, y in data]

    plt.plot(x, y)
    plt.xlabel("Time")
    plt.ylabel("Value")
    plt.title(title)
    plt.show()



if __name__ == '__main__':
    # CBDA
    cbda = CBDA()
    delta = 0.01
    rkf45 = transformToRKF(cbda, delta_t=0.01, start_time=1e-4, atol=2e-5, hmin=0.1, safety=0.84)
    #run(cbda, 10, delta, f"delta={delta}")
    run(cbd=rkf45, num_steps=10, delta_t=delta, title=f"RKF45 delta={delta}", RKF=True)

    # CBDB
    cbdb = CBDB()
    delta = 0.1
    #run(cbdb, 10, delta, f"delta={delta}")

    # Sin(t)
    sin = SinGen()
    delta = 0.1
    #run(sin, 10, delta, f"delta={delta}")

    # ErrorA
    #errA = errorA()
    #delta = 0.1
    #run(errA, 10, delta, f"delta={delta}")

    # ErrorB
    #errB = errorB()
    #delta = 0.1
    #run(errB, 10, delta, f"delta={delta}")

    #checkValitidyLatex(cbda)









