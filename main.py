from CBD.Core import *
from CBD.lib.std import *
from CBD.preprocessing.butcher import ButcherTableau as BT
from CBD.preprocessing.rungekutta import RKPreprocessor
from util import *

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




def transformToRKF(model, delta_t, start_time, atol, hmin, safety):
    model.addFixedRateClock("clock", delta_t=delta_t, start_time=start_time)

    tableau = BT.RKF45()
    RKP = RKPreprocessor(tableau, atol=atol, hmin=hmin, safety=safety)
    new_model = RKP.preprocess(model)

    return new_model


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
    checkValitidyLatex(cbda)

