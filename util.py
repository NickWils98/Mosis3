from CBD.simulator import Simulator
import matplotlib.pyplot as plt
from CBD.converters.latexify.CBD2Latex import CBD2Latex
from CBD.converters.CBDDraw import gvDraw


def checkValitidyLatex(model):
    cbd2latex = CBD2Latex(model, show_steps=True, render_latex=False)

    cbd2latex.simplify()

    # print the resulting equations
    print("RESULT IS:")
    print(cbd2latex.render())

def multiplePlot(_cbda, _cbdb, _sin):
    sim1 = Simulator(_cbda)
    sim1.setDeltaT(0.1)
    sim1.run(50)
    data = _cbda.getSignalHistory('OUT1')
    cbda = [x for x, _ in data], [y for _, y in data]

    sim2 = Simulator(_cbdb)
    sim2.setDeltaT(0.1)
    sim2.run(50)
    data = _cbdb.getSignalHistory('OUT1')
    cbdb = [x for x, _ in data], [y for _, y in data]

    sim3 = Simulator(_sin)
    sim3.setDeltaT(0.1)
    sim3.run(50)
    data = _sin.getSignalHistory('OUT1')
    sin = [x for x, _ in data], [y for _, y in data]

    # Plotting both the curves simultaneously
    plt.plot(cbda[0], cbda[1], color='r', label='cbda')
    plt.plot(cbdb[0], cbdb[1], color='g', label='cbdb')
    plt.plot(sin[0], sin[1], color='b', label='sin')

    # Naming the x-axis, y-axis and the whole graph
    plt.xlabel("Value")
    plt.ylabel("Time")
    plt.title(f"delta{0.1}")

    # Adding legend, which helps us recognize the curve according to it's color
    plt.legend()

    # To load the display window
    plt.show()

def run(cbd, num_steps, delta_t, title, RKF=False, filename=None):
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
    if filename is None:
        plt.show()
    else:
        plt.savefig(filename)
        plt.show()