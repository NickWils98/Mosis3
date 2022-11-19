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
        # self.addBlock(forward_euler_method("integrator"))
        # self.addBlock(forward_euler_method("integrator2"))
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

class test(CBD):
    def __init__(self, name="test"):
        CBD.__init__(self, name, input_ports=[], output_ports=["OUT1"])


        # Add all blocks
        self.addBlock(TimeBlock(block_name="clock"))
        # self.addBlock(IntegratorBlock("integrator"))
        # self.addBlock(forward_euler_method("integrator"))
        self.addBlock(simpson_1_3_rule("integrator"))
        # self.addBlock(trapezoid_rule("integrator"))
        # self.addBlock(Delay("integrator"))
        self.addBlock(ConstantBlock(block_name="ic", value=0))
        # Connect them together
        self.addConnection("ic", "integrator", input_port_name="IC")
        self.addConnection("clock", "integrator", input_port_name="IN1", output_port_name="OUT1")
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
    def __init__(self, block_name):
        CBD.__init__(self, block_name, ["IN1", "IC"], ["OUT1"])
        self.addBlock(ConstantBlock(block_name="zero", value=0))
        self.addBlock(DeltaTBlock(block_name="delta_t"))
        self.addBlock(ProductBlock(block_name="multDelta"))
        self.addBlock(DelayBlock(block_name="delayState"))
        self.addBlock(AdderBlock(block_name="sumState"))

        self.addConnection("IN1", "multDelta")
        self.addConnection("delta_t", "multDelta")
        self.addConnection("multDelta", "sumState")
        self.addConnection("IC", "delayState", input_port_name="IC")
        self.addConnection("delayState", "sumState")
        self.addConnection("sumState", "delayState", input_port_name="IN1")
        self.addConnection("sumState", "OUT1")


class trapezoid_rule(CBD):
    def __init__(self, block_name):
        CBD.__init__(self, block_name, ["IN1", "IC"], ["OUT1"])
        self.addBlock(ConstantBlock(block_name="zero", value=0))
        self.addBlock(ConstantBlock(block_name="half", value=0.5))
        self.addBlock(DelayBlock(block_name="delayIn"))
        self.addBlock(DeltaTBlock(block_name="delta_t"))
        self.addBlock(ProductBlock(block_name="multDelta"))
        self.addBlock(ProductBlock(block_name="division"))
        self.addBlock(DelayBlock(block_name="delayState"))
        self.addBlock(AdderBlock(block_name="sumState"))
        self.addBlock(AdderBlock(block_name="sumInstance"))

        self.addConnection("zero", "delayIn", input_port_name="IC")
        self.addConnection("IN1", "delayIn", input_port_name="IN1")
        self.addConnection("IN1", "sumInstance")
        self.addConnection("delayIn", "sumInstance")
        self.addConnection("sumInstance", "division")
        self.addConnection("half", "division")

        self.addConnection("division", "multDelta")
        self.addConnection("delta_t", "multDelta")
        self.addConnection("multDelta", "sumState")
        self.addConnection("IC", "delayState", input_port_name="IC")
        self.addConnection("delayState", "sumState")
        self.addConnection("sumState", "delayState", input_port_name="IN1")
        self.addConnection("sumState", "OUT1")


class Delay(CBD):
    def __init__(self, block_name):
        CBD.__init__(self, block_name, ["IN1", "IC"], ["OUT1"])
        self.addBlock(ConstantBlock(block_name="zero", value=0))
        self.addBlock(ConstantBlock(block_name="zero2", value=0))
        self.addBlock(DeltaTBlock(block_name="delta_t"))
        self.addBlock(DelayBlock(block_name="delayIn"))
        self.addBlock(DelayBlock(block_name="delayIn2"))
        self.addBlock(ProductBlock(block_name="multDelta"))
        self.addBlock(DelayBlock(block_name="delayState"))
        self.addBlock(AdderBlock(block_name="sumState"))

        self.addConnection("zero", "delayIn", input_port_name="IC")
        self.addConnection("IN1", "delayIn", input_port_name="IN1")
        self.addConnection("zero2", "delayIn2", input_port_name="IC")
        self.addConnection("delayIn", "delayIn2", input_port_name="IN1")
        self.addConnection("delayIn2", "multDelta")
        self.addConnection("delta_t", "multDelta")
        self.addConnection("multDelta", "sumState")
        self.addConnection("IC", "delayState", input_port_name="IC")
        self.addConnection("delayState", "sumState")
        self.addConnection("sumState", "delayState", input_port_name="IN1")
        self.addConnection("sumState", "OUT1")

class simpson_1_3_rule(CBD):
    def __init__(self, block_name):
        CBD.__init__(self, block_name, ["IN1", "IC"], ["OUT1"])
        self.addBlock(ConstantBlock(block_name="zero", value=0))
        self.addBlock(ConstantBlock(block_name="zero2", value=0))
        self.addBlock(ConstantBlock(block_name="zero3", value=1))
        self.addBlock(ConstantBlock(block_name="four", value=4))
        self.addBlock(ConstantBlock(block_name="three", value=2))
        self.addBlock(ConstantBlock(block_name="two", value=2))
        self.addBlock(ConstantBlock(block_name="two2", value=2))
        self.addBlock(ConstantBlock(block_name="third", value=1/3))
        self.addBlock(DelayBlock(block_name="delayIn"))
        self.addBlock(DelayBlock(block_name="delayIn2"))
        self.addBlock(DeltaTBlock(block_name="delta_t"))
        self.addBlock(ProductBlock(block_name="multDelta"))
        self.addBlock(ProductBlock(block_name="division"))
        self.addBlock(ProductBlock(block_name="division2"))
        self.addBlock(ProductBlock(block_name="multfour"))
        self.addBlock(DelayBlock(block_name="delayState"))
        self.addBlock(AdderBlock(block_name="sumState"))
        self.addBlock(AdderBlock(block_name="sumInstance"))
        self.addBlock(AdderBlock(block_name="sumInstance3"))
        self.addBlock(AdderBlock(block_name="sumInstance2"))
        self.addBlock(AdderBlock(block_name="sumInstance4"))
        self.addBlock(DelayBlock(block_name="delayModulo"))
        self.addBlock(AddOneBlock(block_name="addOne"))
        self.addBlock(ModuloBlock(block_name="modulo"))
        self.addBlock(ProductBlock(block_name="multmodulo"))
        self.addBlock(ProductBlock(block_name="multequal"))
        self.addBlock(EqualsBlock(block_name="equal"))

        self.addConnection("zero", "delayIn", input_port_name="IC")
        self.addConnection("IN1", "delayIn", input_port_name="IN1")
        self.addConnection("zero2", "delayIn2", input_port_name="IC")
        self.addConnection("delayIn", "delayIn2", input_port_name="IN1")

        self.addConnection("four", "multfour")
        self.addConnection("delayIn", "multfour")
        self.addConnection("IN1", "sumInstance")
        self.addConnection("multfour", "sumInstance")
        self.addConnection("sumInstance", "sumInstance2")
        self.addConnection("delayIn2", "sumInstance2")
        self.addConnection("sumInstance2", "division")
        self.addConnection("third", "division")
        self.addConnection("division", "multDelta")
        self.addConnection("delta_t", "multDelta")

        self.addConnection("zero3", "delayModulo", input_port_name="IC")
        self.addConnection("addOne", "delayModulo")
        self.addConnection("delayModulo", "addOne")
        self.addConnection("delayModulo","modulo", input_port_name="IN1")
        self.addConnection("two","modulo", input_port_name="IN2")
        self.addConnection("modulo", "multmodulo")
        self.addConnection("multDelta", "multmodulo")

        self.addConnection("IN1", "sumInstance3")
        self.addConnection("delayIn", "sumInstance3")
        self.addConnection("sumInstance3", "division2")
        self.addConnection("two2", "division2")

        self.addConnection("three", "equal")
        self.addConnection("delayModulo", "equal")
        self.addConnection("equal", "multequal")
        self.addConnection("division2", "multequal")


        self.addConnection("multmodulo", "sumState")
        self.addConnection("IC", "delayState", input_port_name="IC")
        self.addConnection("delayState", "sumState")
        self.addConnection("sumState", "delayState", input_port_name="IN1")
        self.addConnection("sumState", "sumInstance4")
        self.addConnection("multequal", "sumInstance4")
        self.addConnection("sumInstance4", "OUT1")


class G_t(CBD):
    def __init__(self, block_name):
        CBD.__init__(self, block_name, ["IN1"], ["OUT1"])
        self.addBlock(ConstantBlock(block_name="one", value=1))
        self.addBlock(ConstantBlock(block_name="two", value=2))
        self.addBlock(PowerBlock(block_name="power"))
        self.addBlock(ProductBlock(block_name="multi"))
        self.addBlock(InverterBlock(block_name="invert"))
        self.addBlock(AdderBlock(block_name="sum"))

        self.addConnection("IN1", "power", input_port_name="IN1")
        self.addConnection("two", "power", input_port_name="IN2")
        self.addConnection("power", "sum")
        self.addConnection("one", "sum")
        self.addConnection("sum", "invert")
        self.addConnection("invert", "multi")
        self.addConnection("IN1", "multi")
        self.addConnection("multi", "OUT1")


class testG_t(CBD):
    def __init__(self, block_name="testgt"):
        CBD.__init__(self, block_name, [], ["OUT1"])
        self.addBlock(TimeBlock(block_name="time"))
        self.addBlock(trapezoid_rule(block_name="integrator"))
        self.addBlock(G_t(block_name="gt"))
        self.addBlock(ConstantBlock(block_name="const", value=0))

        self.addConnection("time", "gt")
        self.addConnection("const", "integrator", input_port_name="IC")
        self.addConnection("gt", "integrator")
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
    # run(cbda, 50, delta, f"CBDA delta={delta}")
    # run(cbd=cbda_rkf45, num_steps=10, delta_t=delta, title=f"CBD_A RKF45 delta={delta}", RKF=True)

    # ===============================================CBD_B==============================================================
    cbdb = CBDB()
    delta = 0.01
    # run(cbdb, 50, delta, f"CBD B delta={delta}")

    # ================================================SIN===============================================================
    sin = SinGen()
    delta = 0.1
    # run(sin, 50, delta, f"SIN delta={delta}")

    # ===============================================ERR_A==============================================================
    errA = errorA()
    delta = 0.01
    # run(errA, 50, delta, f"ERR A delta={delta}")

    # ===============================================ERR_B==============================================================
    errB = errorB()
    delta = 0.01
    # run(errB, 50, delta, f"ERR B delta={delta}")

    # ==============================================VALIDITY============================================================
    # checkValitidyLatex(cbda)

    t = test()
    delta = 1
    # run(t, 6, delta, f"test")

    gt = testG_t()
    delta = 1
    run(gt, 100, delta, f"gt")
    print(gt.getSignalHistory("OUT1"))
    # from CBD.converters.CBDDraw import gvDraw
    # tes = simpson_1_3_rule("sim")
    # gvDraw(tes, "test.gv")
