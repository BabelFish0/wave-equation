import general_wave as wave
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import random
import math

model = wave.Model()
pos_vel_init = wave.Initializer()
model.useDefaultParams()
model.params['total_frames'] = 3
# model.params['wave_speed'] = [10]*300 + [30]*400 + [10]*300
model.params['tension'] = [1]*1000
model.params['mass_density'] = [0.01]*300 + [1/900]*400 + [0.01]*300
model.params['wave_speed'] = [math.sqrt(model.params['tension'][i]/model.params['mass_density'][i]) for i in range(len(model.params['tension']))]
model.init_pos, model.init_vel = pos_vel_init.gauss(velocity=model.params['wave_speed'], shift=50, width=10)
model.init_model()

#init fig and axes
fig = plt.figure()
ax = plt.axes()
line, = ax.plot([], [])
ax.set_ylim(-2, 2)
ax.set_xlim(0, model.params['length'])
ax.set_xlabel(r'$x_i$')
ax.set_ylabel(r'$y(x_i, t_j)$')

tps = 500 #sim speed
fps = 30 #frame rate

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
    print(model.e)

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