import time #Sleep

import mido #Trabalhar com arquivos MID
import numpy as np #Computação numérica
from matplotlib import pyplot as plt #Plotar dados

from markov import Markov
from mid import MID_Handler
from utils import plot_2dhistogram


ORIGINAL = 0
ESTATICO = 1
ALTERNANDO = 2
EST_ALT = 3
ESTATISTICO = 4

def gera_tempo(tipo):

    states = mid_handler.time_states
    original_time_sequence = mid_handler.time_sequence

    transition = None

    markov = Markov()

    if tipo == ORIGINAL:
        return original_time_sequence
    elif tipo == ESTATICO:
        histogram = np.random.uniform(0,1,(5,5))
        histogram += np.eye(5)*100

        states = np.linspace(0.1,0.5,5)

        mid_handler.time_states = states
        transition = markov.from_histogram(histogram, states)
    
    elif tipo == ALTERNANDO:
        histogram = np.random.uniform(0,1,(4,4))
        histogram += np.rot90(np.eye(4)*100)

        states = np.linspace(0.1,0.5,4)

        mid_handler.time_states = states
        transition = markov.from_histogram(histogram, states)
    
    elif tipo == EST_ALT:
        histogram = np.random.uniform(0,1,(4,4))
        histogram += np.eye(4)*100
        histogram += np.rot90(np.eye(4)*50)

        states = np.linspace(0.1,0.5,4)

        mid_handler.time_states = states
        transition = markov.from_histogram(histogram, states)

    elif tipo == ESTATISTICO:
        transition, histogram = markov.from_state_sequence(original_time_sequence, states)

    
    plot_2dhistogram(transition, states, "Matriz de transição", 
                                        "Próximo estado",
                                        "Estado anterior", True)

    return markov.generate_states(len(original_time_sequence))
    

        
if __name__ == "__main__":

    mid_folder = "Músicas MID\\"

    port = mido.open_output(mido.get_output_names()[0])
    #mid = mido.MidiFile("Howl’s_Moving_Castle_-_Merry_go_round.mid")
    #mid = mido.MidiFile("Yuri on ICE.mid")
    mid = mido.MidiFile(mid_folder+"cs1-1pre.mid")
    #mid = mido.MidiFile("Apotheosis_Midi.mid")

    mid_handler = MID_Handler(mid)
    original_time_sequence = mid_handler.time_sequence

    #plot_2dhistogram(histogram, states, "Histograma das transições originais", 
    #                                    "Próximo estado",
    #                                    "Estado anterior", True)

    
    new_time_sequence = gera_tempo(EST_ALT)

    mid_handler.time_sequence = new_time_sequence

    plt.title("Tempos do arquivo")
    plt.plot(original_time_sequence)
    plt.plot(new_time_sequence, alpha=0.75)
    plt.legend(["Tempo original","Novo tempo"])
    plt.show()

    mid_handler.play(port)

    #mid_handler.save("markov_result.mid")