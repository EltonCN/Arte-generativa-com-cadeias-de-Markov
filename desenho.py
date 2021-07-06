import numpy as np

from markov import Markov
from utils import plot_2dhistogram
from turtle import TurtleGraph

markov = Markov()
turtle = TurtleGraph()

opt = "circular_pattern"

if opt == "random":

    n_state = len(TurtleGraph.command_list)

    hist = np.random.uniform(0,100,(n_state,n_state))

    hist[:,TurtleGraph.command_list.index("F")] *= 1
    hist[:, TurtleGraph.command_list.index("ANGLE")] /= 5
    hist[:, TurtleGraph.command_list.index("DIST")] /= 5

    markov.from_histogram(hist, np.array(TurtleGraph.command_list))

else:
    for command in TurtleGraph.command_list:
        markov.add_states(command)

    if opt == "square":
        markov.transition_prob("F","R", 1.0)
        markov.transition_prob("R","F", 1.0)

        for command in TurtleGraph.command_list:
            if command != "F" and command != "R":
                markov.transition_prob(command, "F", 1.0)
            turtle.parameter_change(False)

    elif opt == "circular_pattern":
        markov.transition_prob("L","ANGLE", 0.5)
        markov.transition_prob("L","DIST", 0.5)

        markov.transition_prob("ANGLE","R", 1.0)
        markov.transition_prob("DIST","F", 1.0)

        markov.transition_prob("F","R", 1.0)        
        markov.transition_prob("R","F", 1.0)

        markov.transition_prob("F","R", 0.9)        
        markov.transition_prob("R","F", 0.9)

        markov.transition_prob("F","ANGLE", 0.1)
        markov.transition_prob("R","DIST", 0.1)



sequence = markov.generate_states(1000)
#print(sequence)



plot_2dhistogram(markov.transition,TurtleGraph.command_list,"Matriz de Transição", 
                                        "Próximo estado",
                                        "Estado anterior", False)


turtle.run_sequence(sequence)
turtle.plot()