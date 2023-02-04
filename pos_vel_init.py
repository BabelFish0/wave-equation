import math
import numpy as np

#position and velocity functions
def init_pos_bell(x_size, x_scaling, y_scaling):
    '''A possible starting shape'''
    return [y_scaling*math.e**(-1*(((x-x_size/2)*x_scaling)**2)) for x in range(x_size)]

def init_vel_discont(width, x_size, y_scaling):
    '''Discontinuous starting velocity function'''
    if width%2 != x_size%2:
        print('width and x_size must both be even or both be odd!')
        return
    padding = [0]*int((x_size-width)/2)
    return padding + [y_scaling]*width + padding

#string init functions
def bell_at_rest(x_size, x_scaling, y_scaling):
    initial_pos = init_pos_bell(x_size, x_scaling, y_scaling) #bell curve at rest
    initial_vel = [0]*len(initial_pos)
    y_min, y_max = -max(initial_pos), max(initial_pos)
    return initial_pos, initial_vel, y_min, y_max

def flat_struck(x_size, width, y_scaling):
    initial_vel = init_vel_discont(width, x_size, y_scaling)#flat line with middle region struck
    initial_pos = [0]*len(initial_vel)
    y_min, y_max = -y_scaling*10, y_scaling*10
    return initial_pos, initial_vel, y_min, y_max