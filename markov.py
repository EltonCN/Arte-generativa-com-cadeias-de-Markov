import random

import numpy as np

class Markov():

    def __init__(self):
        self.states = {}
        self.transition = np.ndarray(0,dtype=np.float64)
        self.cumulative = None

        self.states_list = None


    # 1 - func add estado -> add linha add coluna na matriz de transição, add no dict de estados
    def add_states(self, state):
        self.states[state]=len(self.transition) 

        size = self.transition.shape[0]
        self.transition.resize((size+1, size+1))
        
        self.states_list = list(self.states.keys())
        self.cumulative = None

    # 2 - func gera a matriz de probabilidades acumuladas -> pra cada linha da matriz somar as probab
    # das colunas anteriores, se a col == zero, deixa zero 
    def create_prob_matrix(self):
        
        matrix = np.zeros_like(self.transition)
        
        for r in range(len(self.transition)):
            sum = 0.0
            for c in range(len(self.transition[0])):
                sum += self.transition[r][c]
                if self.transition[r][c] != 0:
                    matrix[r][c] = sum
        
        self.cumulative = matrix

    # 3 - func define a probabilidade de uma transição, recebe o estado de entrada, saida e a prob
    #prob 0<=p<=1, os dois estados precisam estar no dict 
    def transition_prob(self, state_prev, state_next, prob):
        prev = self.states[state_prev]
        next = self.states[state_next]
        self.transition[prev][next] = prob

        self.cumulative = None
        
        
    # 4 - func gera uma sequencia de estados de tamanho N
    def generate_states(self, n):
        '''
            Creates a random sequence of states,
            using the transition matrix.

            Parameters:
                n: size of the sequence
        '''

        if self.cumulative is None:
            self.create_prob_matrix()

        #plot_2dhistogram(self.cumulative, self.states_list)
        #print(self.cumulative)

        sequence = []
        state = random.choice(self.states_list)
        line = self.states[state]

        sequence.append(state)

        while len(sequence) < n:
            prob = np.random.uniform(0,1,1)[0]

            for i in range(len(self.cumulative)):

                #print(self.cumulative[line][i], prob)

                if self.cumulative[line][i] >= prob and self.cumulative[line][i] != 0:
                    state = self.states_list[i]
                    sequence.append(state)
                    line = i
                    break

            #exit(0)
        return sequence


    def from_state_sequence(self, sequence, states):
        '''
            Generates the transition matrix using the
            histogram from a sequence of states

            Parameters:
                sequence: the sequence of states
                states: list of possible states
            
            Returns:
                transition: transition matrix from the histogram
                histogram: histogram of state changes on the sequence
        '''

        n_state = states.shape[0]
        histogram = np.zeros((n_state, n_state), np.float64)

        states_dict = {}

        for i in range(n_state):
            states_dict[states[i]] = i

        for i in range(1, sequence.shape[0]):
            prev_state = sequence[i-1]
            prev_state_index = states_dict[prev_state]

            next_state = sequence[i]
            next_state_index = states_dict[next_state]

            histogram[prev_state_index][next_state_index] += 1
        
        transition = self.from_histogram(histogram, states)

        return transition, histogram
    
    def from_histogram(self, histogram, states):

        transition = histogram.copy()

        n_state = states.shape[0]

        states_dict = {}

        for i in range(n_state):
            states_dict[states[i]] = i

        for i in range(transition.shape[0]):
            transition[i] /= np.sum(histogram[i])

        self.transition = transition
        self.states = states_dict
        self.states_list = list(states_dict.keys())
        
        return transition


