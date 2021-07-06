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

def get_subtitulo(tipo):
    subtitulo = "Tempo "

    if tipo == ORIGINAL:
        subtitulo += "Original"
    elif tipo == ESTATICO:
        subtitulo += "Estático"
    elif tipo == ALTERNANDO:
        subtitulo += "Alternando"
    elif tipo == EST_ALT:
        subtitulo += "Estático Alternando"
    elif tipo == ESTATISTICO:
        subtitulo += "Estatístico"

    return subtitulo


def gera_tempo(tipo, nome_musica):

    states = mid_handler.time_states
    original_time_sequence = mid_handler.time_sequence

    transition = None

    subtitulo = get_subtitulo(tipo)

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

    
    plot_2dhistogram(transition, states, "Matriz de transição - "+nome_musica, 
                                        "Próximo estado",
                                        "Estado anterior", True, subtitulo)

    return markov.generate_states(len(original_time_sequence))
    

MUSICA = "Ghosts of Reach"
  
if __name__ == "__main__":

    mid_folder = "Músicas MID\\"
    
    port = mido.open_output(mido.get_output_names()[0])

    mid = None

    if MUSICA == "Bach - Suite 1 em G maior":
        #Bach Suit 1 em G maior
        mid = mido.MidiFile(mid_folder+"cs1-1pre.mid")
    else:
        #Halo
        mid = mido.MidiFile(mid_folder+"02 - MIDI - Ghosts of Reach.mid")

    mid_handler = MID_Handler(mid)
    original_time_sequence = mid_handler.time_sequence

    
    #ORIGINAL = Tempos originais
    #ESTATISTICO = Tempos gerados usando o histograma gerado pela música
    #ESTATICO = Tempos gerados para ficar sempre no mesmo
    #ALTERNANDO = Tempos alternandos
    #EST_ALT = Tempos gerados para ficar alternando ou sempre no mesmo tempo

    tipo = ESTATISTICO

    new_time_sequence = gera_tempo(tipo, MUSICA)

    mid_handler.time_sequence = new_time_sequence

    subtitulo = get_subtitulo(tipo)

    fig = plt.figure()
    plt.suptitle("Tempos da música")
    plt.title(MUSICA+" - "+subtitulo)
    plt.plot(original_time_sequence)
    plt.plot(new_time_sequence, alpha=0.75)
    plt.legend(["Tempo original","Novo tempo"])
    plt.show()
    fig.savefig("Tempos do arquivo - "+MUSICA+" - "+subtitulo+".jpg")

    mid_handler.play(port)
