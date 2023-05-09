import general_wave as wave
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import random
import math
import csv
import numpy as np

init_amplitude = 0.001

model = wave.Model()
pos_vel_init = wave.Initializer()
model.useDefaultParams()
model.params['total_frames'] = 3
# model.params['wave_speed'] = [10]*300 + [30]*400 + [10]*300
model.params['tension'] = [1]*1000
model.params['mass_density'] = [0.01]*500 + model.generate_random_sections(500, 50, 10)#model.generate_alternating_sections(500, 50, 0.01, 0.001)#[0.01]*500 + [0.005]*500#[0.01]*450 + [0.005]*100 + [0.001]*450
model.params['wave_speed'] = [math.sqrt(model.params['tension'][i]/model.params['mass_density'][i]) for i in range(len(model.params['tension']))]
model.init_pos, model.init_vel = pos_vel_init.gauss(amplitude=init_amplitude, velocity=model.params['wave_speed'], shift=150, width=20)
model.init_model()
starting_e = model.e

#init fig and axes
fig = plt.figure()
ax = plt.axes()
line, = ax.plot([], [])
dy_dx_line, = ax.plot([], [])
d2y_dx2_line, = ax.plot([], [])
d2y_dt2_line, = ax.plot([], [])
ax.set_ylim(-2*init_amplitude, 2*init_amplitude)
ax.set_xlim(0, model.params['length'])
ax.set_xlabel(r'$x_i$')
ax.set_ylabel(r'$y(x_i, t_j)$')

tps = 500 #sim speed
fps = 30 #frame rate

amplitude_record = [[], []]



def init():
    '''Function to reset animation'''
    line.set_data([], [])
    dy_dx_line.set_data([], [])
    d2y_dx2_line.set_data([], [])
    d2y_dt2_line.set_data([], [])
    return line, #dy_dx_line, #d2y_dt2_line, d2y_dx2_line

def update_derivative_data():
    return (model.dy_dx, model.d2y_dx2, model.d2y_dt2)

def reset_model(rho1, rho2):
    model.params['mass_density'] = [rho1]*500 + [rho2]*500
    model.params['wave_speed'] = [math.sqrt(model.params['tension'][i]/model.params['mass_density'][i]) for i in range(len(model.params['tension']))]
    model.init_pos, model.init_vel = pos_vel_init.gauss(amplitude=init_amplitude, velocity=model.params['wave_speed'], shift=100, width=10)
    model.init_model()

def animate(i):
    global tps
    global fps
    global amplitude_record
    global init_amplitude
    #set graph data
    graphX = model.get_all_x_positions()
    graphY = model.y[:, 1] #all y(x_i) for current timestep
    print(round(model.e/starting_e, 4))

    #update graph with said data
    line.set_data(graphX, graphY)
    # dy_dx, d2y_dx2, d2y_dt2 = update_derivative_data()
    # dy_dx_line.set_data(graphX[1:-1], dy_dx)
    # d2y_dx2_line.set_data(graphX[1:-1], d2y_dx2)
    # d2y_dt2_line.set_data(graphX[1:-1], d2y_dt2)

    #run the simulation for a certain number of timesteps per frame (retains accuracy w/o slow animation)
    for k in range(math.ceil(tps/fps)):
        model.compute_timestep(1) #overwrite next timestep (t_3)
        model.shift_timesteps(-1) #roll timesteps back so that t_0 becomes t_3 in the array

        # if model.has_wave_passed(650, 1): #return details about maxima and restart
        #     print(f'A_R/A_I: {max(model.y[:500, 1])/init_amplitude}, A_T/A_I: {max(model.y[500:, 1])/init_amplitude}, wave speed: ', model.params['wave_speed'][0], model.params['wave_speed'][-1])
        #     amplitude_record[0] += [(max(model.y[:500, 1])/init_amplitude)**2]
        #     amplitude_record[1] += [(max(model.y[500:, 1])/init_amplitude)**2]
        #     reset_model(0.01, model.params['mass_density'][-1]+0.0001)
    return line,

# Run animation
frame_time_ms = 1/fps * 1_000
anim = FuncAnimation(fig, animate, init_func=init, frames=1000, interval=frame_time_ms)#10ms is good for realtime, set to <<1 for rendering

def write_amplitude_data(input_array, filename='output.csv'):
    # Transpose the input array so that it has 2 columns and n rows
    output_array = np.transpose(input_array)

    header = ['(A_R/A_I)^2', '(A_T/A_I)^2']

    with open(str(filename), 'w', newline='') as file:
        writer = csv.writer(file)

        # Write the header row to the csv file
        writer.writerow(header)

        # Write each row of the output array to the csv file
        for row in output_array:
            writer.writerow(row)

#anim.save('wave_anim_random_v.gif')
plt.show()
#write_amplitude_data(amplitude_record)