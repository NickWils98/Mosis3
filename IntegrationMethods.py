from CBD.Core import *
from CBD.lib.std import *
from util import *


class ForwardEulerMethod(CBD):
    def __init__(self, block_name="integrator"):
        CBD.__init__(self, block_name, ["IN1", "IC"], ["OUT1"])

        # Add all blocks
        self.addBlock(DeltaTBlock(block_name="delta_t"))
        self.addBlock(ProductBlock(block_name="multDelta"))
        self.addBlock(DelayBlock(block_name="delayState"))
        self.addBlock(AdderBlock(block_name="sumState"))

        # Connect them together
        self.addConnection("IN1", "multDelta")
        self.addConnection("delta_t", "multDelta")
        self.addConnection("multDelta", "sumState")
        self.addConnection("IC", "delayState", input_port_name="IC")
        self.addConnection("delayState", "sumState")
        self.addConnection("sumState", "delayState", input_port_name="IN1")
        self.addConnection("sumState", "OUT1")

class TrapezoidRule(CBD):
    def __init__(self, block_name="integrator"):
        CBD.__init__(self, block_name, ["IN1", "IC"], ["OUT1"])

        # Add all blocks
        self.addBlock(ConstantBlock(block_name="zero", value=0))
        self.addBlock(ConstantBlock(block_name="half", value=0.5))
        self.addBlock(DelayBlock(block_name="delayIn"))
        self.addBlock(DeltaTBlock(block_name="delta_t"))
        self.addBlock(ProductBlock(block_name="multDelta"))
        self.addBlock(ProductBlock(block_name="division"))
        self.addBlock(DelayBlock(block_name="delayState"))
        self.addBlock(AdderBlock(block_name="sumState"))
        self.addBlock(AdderBlock(block_name="sumInstance"))

        # Connect them together
        # Get the two timestamps
        self.addConnection("zero", "delayIn", input_port_name="IC")
        self.addConnection("IN1", "delayIn", input_port_name="IN1")
        self.addConnection("IN1", "sumInstance")

        # Sum the times divided by two
        self.addConnection("delayIn", "sumInstance")
        self.addConnection("sumInstance", "division")
        self.addConnection("half", "division")

        # multiply by delta t
        self.addConnection("division", "multDelta")
        self.addConnection("delta_t", "multDelta")

        # Sum over all previous values
        self.addConnection("multDelta", "sumState")
        self.addConnection("IC", "delayState", input_port_name="IC")
        self.addConnection("delayState", "sumState")
        self.addConnection("sumState", "delayState", input_port_name="IN1")
        self.addConnection("sumState", "OUT1")


class SimpsonOneThirdRule(CBD):
    def __init__(self, block_name="integrator"):
        CBD.__init__(self, block_name, ["IN1", "IC"], ["OUT1"])

        # Add all blocks
        self.addBlock(ConstantBlock(block_name="zero", value=0))
        self.addBlock(ConstantBlock(block_name="third", value=1/3))
        self.addBlock(ConstantBlock(block_name="one", value=1))
        self.addBlock(ConstantBlock(block_name="two", value=2))
        self.addBlock(ConstantBlock(block_name="four", value=4))

        self.addBlock(DelayBlock(block_name="delayIn"))
        self.addBlock(DelayBlock(block_name="delayIn2"))
        self.addBlock(DelayBlock(block_name="delayState"))
        self.addBlock(DelayBlock(block_name="delayModulo"))

        self.addBlock(DeltaTBlock(block_name="delta_t"))

        self.addBlock(ProductBlock(block_name="multDelta"))
        self.addBlock(ProductBlock(block_name="multSimpson"))
        self.addBlock(ProductBlock(block_name="multIter2"))
        self.addBlock(ProductBlock(block_name="multTrapezoid"))
        self.addBlock(ProductBlock(block_name="division"))
        self.addBlock(ProductBlock(block_name="divisionTrapezoid"))

        self.addBlock(AdderBlock(block_name="sumState"))
        self.addBlock(AdderBlock(block_name="sumSimpson1"))
        self.addBlock(AdderBlock(block_name="sumSimpson2"))
        self.addBlock(AdderBlock(block_name="sumTrapezoid"))
        self.addBlock(AdderBlock(block_name="sumStateTrapezoid"))

        self.addBlock(AddOneBlock(block_name="addOne"))
        self.addBlock(ModuloBlock(block_name="modulo"))
        self.addBlock(EqualsBlock(block_name="equal"))

        # Connect them together
        # Make the two delays
        self.addConnection("zero", "delayIn", input_port_name="IC")
        self.addConnection("IN1", "delayIn", input_port_name="IN1")
        self.addConnection("zero", "delayIn2", input_port_name="IC")
        self.addConnection("delayIn", "delayIn2", input_port_name="IN1")

        # Calculate simpsons 1/3 rule
        self.addConnection("four", "multSimpson")
        self.addConnection("delayIn", "multSimpson")
        self.addConnection("IN1", "sumSimpson1")
        self.addConnection("multSimpson", "sumSimpson1")
        self.addConnection("sumSimpson1", "sumSimpson2")
        self.addConnection("delayIn2", "sumSimpson2")
        self.addConnection("sumSimpson2", "division")
        self.addConnection("third", "division")
        self.addConnection("division", "multDelta")
        self.addConnection("delta_t", "multDelta")

        # Compute only every other iteration
        self.addConnection("one", "delayModulo", input_port_name="IC")
        self.addConnection("addOne", "delayModulo")
        self.addConnection("delayModulo", "addOne")
        self.addConnection("delayModulo", "modulo", input_port_name="IN1")
        self.addConnection("two", "modulo", input_port_name="IN2")
        self.addConnection("modulo", "multIter2")
        self.addConnection("multDelta", "multIter2")

        # Calculate trapezoid rule
        self.addConnection("IN1", "sumTrapezoid")
        self.addConnection("delayIn", "sumTrapezoid")
        self.addConnection("sumTrapezoid", "divisionTrapezoid")
        self.addConnection("two", "divisionTrapezoid")

        # Look if there are only two points, only then use the Trapezoid rule
        self.addConnection("two", "equal")
        self.addConnection("delayModulo", "equal")
        self.addConnection("equal", "multTrapezoid")
        self.addConnection("divisionTrapezoid", "multTrapezoid")

        # Make it ready for the next iteration and output
        self.addConnection("multIter2", "sumState")
        self.addConnection("IC", "delayState", input_port_name="IC")
        self.addConnection("delayState", "sumState")
        self.addConnection("sumState", "delayState", input_port_name="IN1")
        self.addConnection("sumState", "sumStateTrapezoid")
        self.addConnection("multTrapezoid", "sumStateTrapezoid")
        self.addConnection("sumStateTrapezoid", "OUT1")

class G_t(CBD):
    def __init__(self, block_name="G_T"):
        CBD.__init__(self, block_name, ["IN1"], ["OUT1"])

        # Add all blocks
        self.addBlock(ConstantBlock(block_name="one", value=1))
        self.addBlock(ConstantBlock(block_name="two", value=2))
        self.addBlock(PowerBlock(block_name="power"))
        self.addBlock(ProductBlock(block_name="multi"))
        self.addBlock(InverterBlock(block_name="invert"))
        self.addBlock(AdderBlock(block_name="sum"))

        # Connect them together
        self.addConnection("IN1", "power", input_port_name="IN1")
        self.addConnection("two", "power", input_port_name="IN2")
        self.addConnection("power", "sum")
        self.addConnection("one", "sum")
        self.addConnection("sum", "invert")
        self.addConnection("invert", "multi")
        self.addConnection("IN1", "multi")
        self.addConnection("multi", "OUT1")

class IntegralOfGt(CBD):
    def __init__(self, integrator=IntegratorBlock, block_name="IntegralOfGt"):
        CBD.__init__(self, block_name, [], ["OUT1"])

        # Add all blocks
        self.addBlock(TimeBlock(block_name="time"))
        self.addBlock(integrator(block_name="integrator"))
        self.addBlock(G_t(block_name="gt"))
        self.addBlock(ConstantBlock(block_name="zero", value=0))

        # Connect them together
        self.addConnection("time", "gt")
        self.addConnection("zero", "integrator", input_port_name="IC")
        self.addConnection("gt", "integrator")
        self.addConnection("integrator", "OUT1")

class testGt(CBD):
    def __init__(self, integrator=IntegratorBlock, block_name="IntegralOfGt"):
        CBD.__init__(self, block_name, [], ["OUT1"])

        # Add all blocks
        self.addBlock(TimeBlock(block_name="time"))
        self.addBlock(integrator(block_name="integrator"))
        self.addBlock(ConstantBlock(block_name="zero", value=0))

        # Connect them together
        self.addConnection("time", "integrator")
        self.addConnection("zero", "integrator", input_port_name="IC")
        self.addConnection("integrator", "OUT1")


if __name__ == '__main__':
    analytic = 4.60522018
    BEM = IntegratorBlock
    FEM = ForwardEulerMethod
    TR = TrapezoidRule
    SOTR = SimpsonOneThirdRule

    deltaList = [0.1, 0.01, 0.001]

    integratorList = [BEM, FEM, TR, SOTR]

    for integrator in integratorList:
        test = testGt(integrator)
        run(test, 5, 1, f"{integrator.__name__} testGt", filename=f"resc/IM/testGt{integrator.__name__}")

    for delta in deltaList:
        for integrator in integratorList:
            print(f"\nIntegrator = {integrator.__name__}", f"Delta = {delta}")
            Gt = IntegralOfGt(integrator, "integrator")
            run(Gt, 100, delta, f"{integrator.__name__} Integral of Gt delta = {delta}", filename=f"resc/IM/{integrator.__name__}{delta}.png")
            print(Gt.getSignalHistory("OUT1")[-1])

    for integratorClass in integratorList:
        print(f"\nIntegrator = {integratorClass.__name__}")
        integrator = integratorClass("integrator")
        checkValitidyLatex(integrator)
        gvDraw(integrator, f"resc/IM/{integrator.__class__.__name__}.gv")

    gvDraw(G_t(), f"resc/IM/G_t.gv")


