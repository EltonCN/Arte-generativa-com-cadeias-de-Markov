import time

import mido
import numpy as np

class MID_Handler:
    '''
        Handle the mid file
    '''

    def __init__(self, mid):
        '''
            MID_Handler constructor

            Parameters:
                mid: the mid file, type must be mido.Midfile
        '''

        self.mid = mid

        self._time_sequence = None
        self._time_states = None

        self._mid_time_sequence = None
        self._mid_time_states = None

    @property
    def time_sequence(self):
        '''
            Sequence of times of the notes
        '''
        if self._time_sequence is None:
            self._time_sequence = self.mid_time_sequence

        return self._time_sequence

    @time_sequence.setter
    def time_sequence(self, new_list):
        self._time_sequence = new_list

    @property
    def time_states(self):
        '''
            Possible time states
        '''
        if self._time_states is None:
            self._time_states = self.mid_time_states

        return self._time_states

    @time_states.setter
    def time_states(self, new_value):
        self._time_states = new_value

    @property
    def mid_time_sequence(self):
        '''
            Default time sequence from file
        '''
        if self._mid_time_sequence is None:
            self.generate_mid_info()
        return self._mid_time_sequence
    
    @property 
    def mid_time_states(self):
        '''
            Default time states from file
        '''
        if self._mid_time_states is None:
            self.generate_mid_info()
        return self._mid_time_states

    
    def generate_mid_info(self):
        '''
            Generates the time states and sequence from the file
        '''

        times = []

        for msg in self.mid:
            times.append(msg.time)

        times = np.array(times)

        time_nonzero = times[np.nonzero(times)]

        time_rounded = np.around(time_nonzero, decimals=1)

        values, counts = np.unique(time_rounded, return_counts=True)

        print(counts)

        threshould = np.ceil(np.power(counts.prod(), 1.0/counts.shape[0]))
        #threshould = np.mean(counts)
        #threshould = 4
        threshould = 5

        states = values[counts>=threshould]
        #states = values
        
        states = states[np.nonzero(states)]

        time_states = time_nonzero.copy()

        for i in range(time_states.shape[0]):
            index = (np.abs(states-time_states[i])).argmin()

            time_states[i] = states[index]
        
        self._mid_time_states = states
        self._mid_time_sequence = time_states

    def play(self, port, max_msg=0):
        '''
            Play the file with assigned times

            Parameters:
                port: mido port to send the mid messages

                max_msg: the number os messages in the file to be played. 
                         If 0, play all messages. Default is 0
        '''

        if self._time_sequence is None:
            self._time_sequence = self.mid_time_sequence

        index = 0
        msg_count = 0

        for msg in self.mid:
            if msg.time != 0:
                time.sleep(self._time_sequence[index])
                index += 1
        
            if not msg.is_meta:
                if not msg.is_cc:
                    #msg = msg.copy(velocity=64)
                    pass
                port.send(msg)
            
            msg_count += 1
            
            if max_msg != 0 and msg_count>max_msg:
                break
        
        port.reset()

    def save(self, file_name):
        file = mido.MidiFile()
        track = mido.MidiTrack()

        file.ticks_per_beat = self.mid.ticks_per_beat

        file.tracks.append(track)

        index = 0

        for msg in self.mid:
            if msg.time != 0:  
                msg = msg.copy(time=int(self._time_sequence[index]*self.mid.ticks_per_beat))
                index += 1

            track.append(msg)
        
        file.save(file_name)
                
    