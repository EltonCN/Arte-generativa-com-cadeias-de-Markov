import numpy as np
from matplotlib import pyplot as plt

class TurtleGraph:
    '''
       A turtle graphics generator

       The existing commands are declared in "command_list":
        F - go forward
        R - turn right
        L - turn left
        DIST - randomly change the forward step
        ANGLE - randomly change the rotation angle
    '''

    command_list = ["F","R","L","DIST","ANGLE"]

    def __init__(self):
        self.position = np.zeros(2, np.float64)
        self.orientation = 0

        self.hist = np.array([self.position.copy()])

        self.dist = 10
        self.angle = np.pi/2.0

        self.change_param = True

    @staticmethod
    def get_rotation(angle):
        '''
            Gets a rotation matrix from a angle

            Parameters:
                angle: rotation angle (rad)

            Returns:
                R: rotation 2x2 matrix
        '''
        R = np.eye(2, dtype=np.float64)

        R *= np.cos(angle)

        R[0,1] = -np.sin(angle)
        R[1,0] = np.sin(angle)

        return R
    

    def run_command(self, command):
        '''
            Run a command for the turtle

            Parameters:
                command: the command that will be run. 
                         Unrecognized commands will do nothing.
                         See class documentation for available commands
        '''

        if command == "F":

            t = np.array([self.dist,0.0], np.float64)


            R = TurtleGraph.get_rotation(self.orientation)

            t = R@t

            

            self.position += t

        elif command == "R":
            self.orientation -= self.angle
        
        elif command == "L":
            self.orientation += self.angle

        elif command == "DIST" and self.change_param:
            self.dist = np.random.uniform(0.5,1, 1)[0]
        elif command == "ANGLE" and self.change_param:
            self.angle = np.random.uniform(0, 2.0*np.pi, 1)[0]
        
        self.hist = np.vstack((self.hist, self.position))

    def run_sequence(self, sequence):
        '''
            Run a sequence of commands for the turtle

            Parameters:
                sequence: list with commands
                          See class documentation for available commands
        '''
        for command in sequence:
            self.run_command(command)

    def plot(self, nome=""):
        '''
            Plots the turtle draw unsing pyplot
        '''
        fig = plt.figure(figsize=(5,5))
        plt.suptitle("Gr??fico tartaruga")
        plt.title(nome)
        plt.plot(self.hist[:,0], self.hist[:,1])
        plt.show()

        return fig

    def parameter_change(self, config):
        '''
            Sets if the distance and angle of draw can be changed
            by a command

            Parameters:
                config: True if the parameters can be changed, False otherwise
        '''
        self.change_param = config



