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

def graph_analitic():
    x_cords = [0.01*x for x in range(0,101)]
    y_cords = [np.exp(x*-15) for x in x_cords]

    plt.plot(x_cords, y_cords)
    plt.savefig(f"resc/SSOE/Yt.png")

    plt.show()

def multiplePlot():
    BEM = IntegratorBlock
    FEM = ForwardEulerMethod
    TR = TrapezoidRule
    SOTR = SimpsonOneThirdRule

    deltaList = [0.25, 0.125, 0.1, 0.05]

    for delt in deltaList:
        ####
        x_cords = [0.01 * x for x in range(0, 101)]
        y_cords = [np.exp(x * -15) for x in x_cords]
        analytic = [x_cords, y_cords]

        ###
        yt1 = Yt(integrator=BEM)
        sim1 = Simulator(yt1)
        sim1.setDeltaT(delt)
        sim1.run(1)
        data = yt1.getSignalHistory('OUT1')
        yt1 = [x for x, _ in data], [y for _, y in data]

        ###
        yt2 = Yt(integrator=FEM)
        sim2 = Simulator(yt2)
        sim2.setDeltaT(delt)
        sim2.run(1)
        data = yt2.getSignalHistory('OUT1')
        yt2 = [x for x, _ in data], [y for _, y in data]

        ###
        yt3 = Yt(integrator=TR)
        sim3 = Simulator(yt3)
        sim3.setDeltaT(delt)
        sim3.run(1)
        data = yt3.getSignalHistory('OUT1')
        yt3 = [x for x, _ in data], [y for _, y in data]

        ###
        yt4 = Yt(integrator=SOTR)
        sim4 = Simulator(yt4)
        sim4.setDeltaT(delt)
        sim4.run(1)
        data = yt4.getSignalHistory('OUT1')
        yt4 = [x for x, _ in data], [y for _, y in data]


        # Plotting both the curves simultaneously
        plt.plot(yt1[0], yt1[1], color='r', label='BEM')
        plt.plot(yt2[0], yt2[1], color='g', label='FEM')
        plt.plot(yt3[0], yt3[1], color='b', label='TR')
        plt.plot(yt4[0], yt4[1], color='c', label='SOTR')
        plt.plot(analytic[0], analytic[1], color='k', label='analytic')

        # Naming the x-axis, y-axis and the whole graph
        plt.xlabel("Value")
        plt.ylabel("Time")
        plt.title(f"delta{delt}")

        if delt == 0.25:
            plt.ylim(-3, 3)

        # Adding legend, which helps us recognize the curve according to it's color
        plt.legend()

        # To load the display window
        plt.savefig(f"resc/SSOE/delta = {delt}.png")
        plt.show()

if __name__ == '__main__':
    deltaList = [0.25, 0.125, 0.1, 0.05]

    BEM = IntegratorBlock
    FEM = ForwardEulerMethod
    TR = TrapezoidRule
    SOTR = SimpsonOneThirdRule

    integratorList = [BEM, FEM, TR, SOTR]

    graph_analitic()

    for delta in deltaList:
        for integrator in integratorList:
            yt = Yt(integrator=integrator)
            run(yt, 1, delta, f"{integrator.__name__} Integral of Yt delta = {delta}", filename=f"resc/SSOE/{integrator.__name__}{delta}.png")

    multiplePlot()
