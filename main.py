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
        self.addBlock(IntegratorBlock("integrator"))
        self.addBlock(IntegratorBlock("integrator2"))
        self.addBlock(ConstantBlock(block_name="ic", value=0))
        self.addBlock(ConstantBlock(block_name="ic2", value=1))
        self.addBlock(NegatorBlock(block_name="negator"))
        # Connect the blocks
        self.addConnection("ic", "integrator", input_port_name="IC")
        self.addConnection("integrator", "integrator2")
        self.addConnection("ic2", "integrator2", input_port_name="IC")
        self.addConnection("integrator2", "negator")
        self.addConnection("negator", "integrator")
        self.addConnection("negator", "OUT1")


class CBDB(CBD):
    def __init__(self, name="CBDB"):
        CBD.__init__(self, name, input_ports=[""], output_ports=["OUT1"])

        # Create the blocks
        self.addBlock(DerivatorBlock("derivator"))
        self.addBlock(DerivatorBlock("derivator2"))
        self.addBlock(ConstantBlock(block_name="ic", value=1))
        self.addBlock(ConstantBlock(block_name="ic2", value=0))
        self.addBlock(NegatorBlock(block_name="neg"))

        # Connect the blocks
        self.addConnection("ic", "derivator", input_port_name="IC")
        self.addConnection("derivator", "derivator2")
        self.addConnection("ic2", "derivator2", input_port_name="IC")
        self.addConnection("derivator2", "neg")
        self.addConnection("neg", "derivator")
        self.addConnection("neg", "OUT1")


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
    def __init__(self, name="ErrorA"):
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
    def __init__(self, name="ErrorA"):
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


class forward_euler_method(CBD):
    """
	The integrator block is a CBD that calculates the integration.
	The block is implemented according to the forward Euler rule.

	.. versionchanged:: 1.4
		Replaced **delta_t** input port with internal :class:`DeltaTBlock`.

	Args:
		block_name (str):   The name of the block.

	:Input Ports:
		- **IN1** -- The input.
		- **IC** -- The initial condition. I.e., this value is outputted
		  at iteration 0.

	:Output Ports:
		**OUT1** -- The integral of the input.
	"""

    def __init__(self, block_name):
        CBD.__init__(self, block_name, ["IN1", "IC"], ["OUT1"])
        self.addBlock(ConstantBlock(block_name="zero", value=0))
        self.addBlock(DeltaTBlock(block_name="delta_t"))
        self.addBlock(DelayBlock(block_name="delayIn"))
        self.addBlock(ProductBlock(block_name="multDelta"))
        self.addBlock(DelayBlock(block_name="delayState"))
        self.addBlock(AdderBlock(block_name="sumState"))

        self.addConnection("zero", "delayIn", input_port_name="IC")
        self.addConnection("IN1", "delayIn", input_port_name="IN1")
        self.addConnection("delayIn", "multDelta")
        self.addConnection("delta_t", "multDelta")
        self.addConnection("multDelta", "sumState")
        self.addConnection("IC", "delayState", input_port_name="IC")
        self.addConnection("delayState", "sumState")
        self.addConnection("sumState", "delayState", input_port_name="IN1")
        self.addConnection("sumState", "OUT1")
        # self.addConnection("zero", "delayIn", input_port_name="IC")
        # self.addConnection("IN1", "delayIn", input_port_name="IN1")
        # self.addConnection("IC", "delayState", input_port_name="IC")
        # self.addConnection("delayState", "sumState")
        # self.addConnection("delta_t", "delayState", input_port_name="IN1")
        #
        # self.addConnection("delayState", "multDelta")
        # self.addConnection("delta_t", "multDelta")
        # self.addConnection("multDelta", "sumState")
        # self.addConnection("sumState", "OUT1")



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
    if RKF == False:
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
    # ===============================================CBD_A==============================================================
    cbda = CBDA()
    delta = 0.01
    # cbda_rkf45 = transformToRKF(cbda, delta_t=0.01, start_time=1e-4, atol=2e-5, hmin=0.1, safety=0.84)
    run(cbda, 50, delta, f"CBDA delta={delta}")
    # run(cbd=cbda_rkf45, num_steps=10, delta_t=delta, title=f"CBD_A RKF45 delta={delta}", RKF=True)

    # ===============================================CBD_B==============================================================
    cbdb = CBDB()
    delta = 0.1
    # run(cbdb, 10, delta, f"CBD B delta={delta}")

    # ================================================SIN===============================================================
    sin = SinGen()
    delta = 0.1
    # run(sin, 10, delta, f"SIN delta={delta}")

    # ===============================================ERR_A==============================================================
    errA = errorA()
    delta = 0.01
    # run(errA, 10, delta, f"ERR A delta={delta}")

    # ===============================================ERR_B==============================================================
    errB = errorB()
    delta = 1
    # run(errB, 50, delta, f"ERR Bdelta={delta}")

    # ==============================================VALIDITY============================================================
    # checkValitidyLatex(errA)
