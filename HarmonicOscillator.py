from CBD.Core import *
from CBD.lib.std import *
from CBD.preprocessing.butcher import ButcherTableau as BT
from CBD.preprocessing.rungekutta import RKPreprocessor
from util import *


class CBDA(CBD):
    def __init__(self, block_name="cbda"):
        CBD.__init__(self, block_name, [], ["OUT1"])

        # Create the blocks
        self.addBlock(IntegratorBlock("integrator"))
        self.addBlock(IntegratorBlock("integrator2"))
        self.addBlock(ConstantBlock(block_name="zero", value=0))
        self.addBlock(ConstantBlock(block_name="one", value=1))
        self.addBlock(NegatorBlock(block_name="negate"))

        # Connect the blocks
        self.addConnection("zero", "integrator", input_port_name="IC")
        self.addConnection("integrator", "integrator2")
        self.addConnection("one", "integrator2", input_port_name="IC")
        self.addConnection("integrator2", "negate")
        self.addConnection("negate", "integrator")
        self.addConnection("negate", "OUT1")


class CBDB(CBD):
    def __init__(self, block_name="cbdb"):
        CBD.__init__(self, block_name, input_ports=[], output_ports=["OUT1"])

        # Create the blocks
        self.addBlock(DerivatorBlock("derivative"))
        self.addBlock(DerivatorBlock("derivative2"))
        self.addBlock(ConstantBlock(block_name="one", value=1))
        self.addBlock(ConstantBlock(block_name="zero", value=0))
        self.addBlock(NegatorBlock(block_name="negate"))

        # Connect the blocks
        self.addConnection("one", "derivative", input_port_name="IC")
        self.addConnection("derivative", "derivative2")
        self.addConnection("zero", "derivative2", input_port_name="IC")
        self.addConnection("derivative2", "negate")
        self.addConnection("negate", "derivative")
        self.addConnection("negate", "OUT1")


class SinGen(CBD):
    def __init__(self, block_name="sinGen"):
        CBD.__init__(self, block_name, input_ports=[], output_ports=["OUT1"])

        # Add the 't' parameter
        self.addBlock(TimeBlock("time"))
        self.addBlock(GenericBlock("sin", block_operator="sin"))

        # Connect them together
        self.addConnection("time", "sin", input_port_name='IN1', output_port_name='OUT1')
        self.addConnection("sin", "OUT1", output_port_name='OUT1')


class errorA(CBD):
    def __init__(self, name="ErrorA"):
        CBD.__init__(self, name, input_ports=[], output_ports=["OUT1"])

        # Add all blocks
        self.addBlock(CBDA(block_name="cbda"))
        self.addBlock(SinGen(block_name="sinGen"))
        self.addBlock(IntegratorBlock("integrator"))
        self.addBlock(ConstantBlock(block_name="zero", value=0))
        self.addBlock(AdderBlock(block_name="minus"))
        self.addBlock(NegatorBlock(block_name="negate"))
        self.addBlock(AbsBlock(block_name="absolute"))

        # Connect them together
        self.addConnection("zero", "integrator", input_port_name="IC")
        self.addConnection("cbda", "negate", input_port_name="IN1", output_port_name="OUT1")
        self.addConnection("sinGen", "minus", input_port_name="IN1", output_port_name="OUT1")
        self.addConnection("negate", "minus", input_port_name="IN2", output_port_name="OUT1")
        self.addConnection("minus", "absolute", input_port_name="IN1", output_port_name="OUT1")
        self.addConnection("absolute", "integrator", input_port_name="IN1", output_port_name="OUT1")
        self.addConnection("integrator", "OUT1")


class errorB(CBD):
    def __init__(self, block_name="ErrorA"):
        CBD.__init__(self, block_name, input_ports=[], output_ports=["OUT1"])

        # Add all blocks
        self.addBlock(CBDB("cbdb"))
        self.addBlock(SinGen("sinGen"))
        self.addBlock(IntegratorBlock("integrator"))
        self.addBlock(ConstantBlock(block_name="zero", value=0))
        self.addBlock(AdderBlock(block_name="minus"))
        self.addBlock(NegatorBlock(block_name="negate"))
        self.addBlock(AbsBlock(block_name="absolute"))

        # Connect them together
        self.addConnection("zero", "integrator", input_port_name="IC")
        self.addConnection("cbdb", "negate", input_port_name="IN1", output_port_name="OUT1")
        self.addConnection("sinGen", "minus", input_port_name="IN1", output_port_name="OUT1")
        self.addConnection("negate", "minus", input_port_name="IN2", output_port_name="OUT1")
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

    CBDList = [CBDA, CBDB, SinGen, errorA, errorB]
    deltaList = [0.1, 0.01, 0.001, 0.001]
    deltaList = [0.1]

    '''for delta in deltaList:
        for CBD2 in CBDList:
            print(f"CBD = {CBD2.__name__}", f"Delta = {delta}")
            max_time = 10
            if CBD2 in [errorA, errorB]:
                max_time = 50
            run(CBD2(), max_time, delta, f"{CBD2.__name__} with delta={delta}", filename=f"resc/HO/{CBD2.__name__}{delta}.png")

    for CBD2 in CBDList:
        print(f"\CBD image = {CBD2.__name__}")
        cbd = CBD2("CBD")
        gvDraw(cbd, f"resc/HO/{cbd.__class__.__name__}.gv")

    for CBD2 in CBDList:
        print(f"\nCBD validity = {CBD2.__name__}")
        cbd = CBD2()
        checkValitidyLatex(cbd)'''


    checkValitidyLatex(errorB())


    #cbda_rkf45 = transformToRKF(CBDA(), delta_t=0.1, start_time=1e-4, atol=2e-5, hmin=0.1, safety=0.84)
    #run(cbd=cbda_rkf45, num_steps=10, delta_t=0.1, title=f"CBD_A RKF45 delta={0.1}", RKF=True)