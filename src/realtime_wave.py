import general_wave as wave
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import random
import math

model = wave.Model()
model.useDefaultParams()
model.params['total_frames'] = 3
#model.randomize_wave_speed(section_width=100, min_max=(8, 12))
model.params['wave_speed'] = [10]*300 + [30]*400 + [10]*300
model.init_pos = [1*math.e**(-1*(((x-250)*0.1)**2)) for x in range(1000)]
model.init_vel = [-2*model.params['wave_speed'][i] * math.e ** (-(0.1**2)*((i-250)**2)) * (-2*0.1**2*(i-250)) for i in range(1000)]
model.init_model()

#init fig and axes
fig = plt.figure()
ax = plt.axes()
line, = ax.plot([], [])
ax.set_ylim(-2, 2)
ax.set_xlim(0, model.params['length'])
ax.set_xlabel(r'$x_i$')
ax.set_ylabel(r'$y(x_i, t_j)$')

tps = 1000
fps = 30

def init():
    '''Function to reset animation'''
    line.set_data([], [])
    return line,

def animate(i):
    global tps
    global fps
    #set graph data
    graphX = model.get_all_x_positions()
    graphY = model.y[:, 1] #all y(x_i) for current timestep

    #update graph with said data
    line.set_data(graphX, graphY)

    #run the simulation for a certain number of timesteps per frame (retains accuracy w/o slow animation)
    for k in range(math.ceil(tps/fps)):
        model.compute_timestep(1) #overwrite next timestep (t_3)
        model.shift_timesteps(-1) #roll timesteps back so that t_0 becomes t_3 in the array
    return line,

# Run animation
frame_time_ms = 1/fps * 1_000
anim = FuncAnimation(fig, animate, init_func=init, frames=1000, interval=frame_time_ms)#10ms is good for realtime, set to <<1 for rendering

#anim.save('wave_anim_random_v.gif')
plt.show()