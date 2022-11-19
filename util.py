
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
