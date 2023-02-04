import simple_wave as wav
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

#init fig and axes
fig = plt.figure()
ax = plt.axes()
line, = ax.plot([], [])

#init data for wave eqn
delta_x = 0.5
delta_t = 1e-2
wave_speed = 10
total_time = 3 #note this is the frame cache size
x_size = 1000

initial_pos = wav.init_pos_bell(x_size, 0.01, 1)
ax.set_ylim(-max(initial_pos), max(initial_pos))
ax.set_xlim(0, x_size)

global y
y = wav.init_model(total_time, initial_pos, [0]*len(initial_pos), delta_t)

def update_wave(delta_t=delta_t, delta_x=delta_x, wave_speed=wave_speed):
    '''
    Given two previous timesteps of y(x, t), calculate the next, then roll the array back
    so when next called the function will overwrite the oldest timestep.
    '''
    global y
    return [wav.get_next_y(i, 1, y, delta_t, delta_x, wave_speed) for i in range(x_size)]

def init():
    line.set_data([], [])
    return line,

def animate(i, x_size=x_size):
    global y
    graphX = [range(0, x_size)]
    graphY = y[:, 1]
    print('frame: ', i, max(y[:, 1]))
    line.set_data(graphX, graphY)
    for k in range(20):
        y[:, 2] = update_wave()
        y = np.roll(y, -1, axis=1)
    return line,

anim = FuncAnimation(fig, animate, init_func=init, frames=500, interval=10)

anim.save('wave_anim_loop.gif')