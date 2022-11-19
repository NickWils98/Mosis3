from IntegrationMethods import *


class Yt(CBD):
    def __init__(self, block_name="cbda", integrator=IntegratorBlock):
        CBD.__init__(self, block_name, [], ["OUT1"])

        # Create the blocks
        self.addBlock(integrator("integrator"))
        self.addBlock(ConstantBlock(block_name="minFifteenth", value=-1/15))
        self.addBlock(ConstantBlock(block_name="zero", value=0))
        self.addBlock(ProductBlock(block_name="division"))


        # Connect the blocks
        self.addConnection("zero", "integrator", input_port_name="IC")
        self.addConnection("integrator", "division", input_port_name="IN1")
        self.addConnection("minFifteenth", "division", input_port_name="IN2")
        # self.addConnection("integrator2", "negate")
        self.addConnection("division", "integrator")
        self.addConnection("division", "OUT1")


if __name__ == '__main__':
    integrator=IntegratorBlock
    Gt=Yt(integrator=integrator)
    delta=0.1
    run(Gt, 1, delta, f"{integrator.__name__} Integral of Gt delta = {delta}")