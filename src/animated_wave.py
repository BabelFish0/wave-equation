import simple_wave as wav
import pos_vel_init as pv_init
import numpy as np
import math
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from progress.bar import ShadyBar

plt.rcParams['text.usetex'] = True #use TeX for axes labels

#init fig and axes
fig = plt.figure()
ax = plt.axes()
line, = ax.plot([], [])

#init data for wave eqn
delta_x = 0.5
length = 500 #string length
delta_t = 1e-2
wave_speed = 10
total_time = 3 #note this is the frame cache size (only 3 states are stored at a time for the animator)
frame_rate = 60 #frames per second
simulation_speed = 1000 #timesteps per second
total_frames = 500

#create two arrays: initial_pos and initial_vel which hold position and velocity data for every x at t_0.
x_size = int(length/delta_x)
initial_pos, initial_vel, y_min, y_max = pv_init.bell_at_rest(x_size, x_scaling=1e-2, y_scaling=1)

#define view bounds based on starting condition
ax.set_ylim(y_min, y_max)
ax.set_xlim(0, x_size*delta_x)
ax.set_xlabel(r'$x_i$')
ax.set_ylabel(r'$y(x_i, t_j)$')

#information at top of plot
annotation = {'text':['$\Delta t=' + str(delta_t) + '$', '$\Delta x=' + str(delta_x) + '$', '$v =' + str(wave_speed) + '$']} #TODO: add units in correct formatting
annotation['xy'] = [(0.05*x_size*delta_x, y_max-(i+1)*((y_max-0.6*y_max)/len(annotation['text']))) for i in range(len(annotation['text']))]
for i, an_text in enumerate(annotation['text']):
    ax.annotate(an_text, annotation['xy'][i])

global y #all displacement data is held in the array 'y'.
y = wav.init_model(total_time, initial_pos, initial_vel, delta_t)

def init():
    '''Function to reset animation'''
    line.set_data([], [])
    return line,

def animate(i, x_size=x_size, delta_x=delta_x, fps = frame_rate, tps = simulation_speed):
    '''Calculate next frame (called every frame update)'''
    global y
    global bar

    #set graph data
    graphX = [i*delta_x for i in range(0, x_size)] #all positions across string
    graphY = y[:, 1] #all y(x_i) for current timestep

    #update graph with said data
    line.set_data(graphX, graphY)

    #run the simulation for a certain number of timesteps per frame (retains accuracy w/o slow animation)
    for k in range(math.ceil(tps/fps)):
        y[:, 2] = [wav.get_next_y(i, 1, y, delta_t, delta_x, wave_speed) for i in range(x_size)] #overwrite next timestep (t_3)
        y = np.roll(y, -1, axis=1) #roll timesteps back so that t_0 becomes t_3 in the array

    bar.next()
    return line,

# Run animation
bar = ShadyBar('Processing', max=total_frames, suffix='%(index)i/%(max)i %(eta)ds')
frame_time_ms = 1/frame_rate * 1_000
anim = FuncAnimation(fig, animate, init_func=init, frames=total_frames, interval=frame_time_ms)#10ms is good for realtime, set to <<1 for rendering

#anim.save('wave_anim_loop.gif')
bar.finish()
plt.show()