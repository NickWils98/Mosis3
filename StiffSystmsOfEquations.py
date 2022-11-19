from IntegrationMethods import *
import numpy as np

class Yt(CBD):
    def __init__(self, block_name="yt", integrator=IntegratorBlock):
        CBD.__init__(self, block_name, [], ["OUT1"])

        # Create the blocks
        self.addBlock(integrator("integrator"))
        self.addBlock(ConstantBlock(block_name="minFifteen", value=-15))
        self.addBlock(ConstantBlock(block_name="one", value=1))
        self.addBlock(ProductBlock(block_name="multi"))

        # Connect the blocks
        self.addConnection("multi", "integrator")
        self.addConnection("one", "integrator", input_port_name="IC")
        self.addConnection("integrator", "multi", input_port_name="IN1")
        self.addConnection("minFifteen", "multi", input_port_name="IN2")
        self.addConnection("integrator", "OUT1")

def graph_yt():
    x_cords = [0.01*x for x in range(0,101)]
    y_cords = [np.exp(x*-15) for x in x_cords]

    plt.plot(x_cords, y_cords)
    plt.savefig(f"resc/SSOE/Yt.png")

    plt.show()

if __name__ == '__main__':
    deltaList = [0.25, 0.125, 0.1, 0.05]

    BEM = IntegratorBlock
    FEM = ForwardEulerMethod
    TR = TrapezoidRule
    SOTR = SimpsonOneThirdRule

    integratorList = [BEM, FEM, TR, SOTR]

    graph_yt()

    for delta in deltaList:
        for integrator in integratorList:
            yt = Yt(integrator=integrator)
            run(yt, 1, delta, f"{integrator.__name__} Integral of Yt delta = {delta}", filename=f"resc/SSOE/{integrator.__name__}{delta}.png")

