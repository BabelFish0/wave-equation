import simple_wave as wav
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

#init fig and axes
fig = plt.figure()
ax = plt.axes()
line = ax.plot([], [])

#init data for wave eqn
global delta_t
global delta_x
global wave_speed
delta_x = 0.5
delta_t = 1e-2
wave_speed = 10
total_time = 3 #note this is the frame cache size
x_size = 1000
initial_pos = wav.init_pos_bell(x_size, 0.01, 1)

global y
y = wav.init_model(total_time, initial_pos, [0]*len(initial_pos), delta_t)

def update_wave(delta_t, delta_x, wave_speed):
    '''
    Given two previous timesteps of y(x, t), calculate the next, then roll the array back
    so when next called the function will overwrite the oldest timestep.
    '''
    y[:, 3] = [wav.get_next_y(i, 2, y, delta_t, delta_x, wave_speed) for i in range(x_size)]
    return np.roll(y, -1)

def init():
    line.set_data([], [])
    return line

def animate(frame):
    y = update_wave(delta_t, delta_x, wave_speed)
    graphX = [range(0, x_size)]
    graphY = y[:, 2]
    line.set_data(graphX, graphY)
    return line

anim = FuncAnimation(fig, animate, init_func=init,
                               frames=200, interval=20)

plt.show()