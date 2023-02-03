import matplotlib.pyplot as plt
import numpy as np
import math

delta_x = 0.5
delta_t = 1e-2
wave_speed = 10
total_time = 2000*4
x_size = 1000

def init_pos_bell(x_size, x_scaling, y_scaling):
    return [y_scaling*math.e**(-1*(((x-x_size/2)*x_scaling)**2)) for x in range(x_size)]

initial_pos = init_pos_bell(x_size, 0.01, 1)
initial_velocity = [0]*x_size

def init_model(total_time, initial_pos, initial_velocity, delta_t=delta_t):
    '''
    Return an initialised array of correct shape with first
    two timesteps adequately filled for normal calculation.
    '''
    if len(initial_pos) != len(initial_velocity):
        print('oops, len(initial_pos) != len(initial_velocity)')
        return
    
    y = np.zeros(shape=(len(initial_pos), total_time), dtype=np.float64) #num x points, num t steps

    y[:, 0] = [initial_pos[i] - delta_t*initial_velocity[i] for i in range(len(initial_pos))]
    y[:, 1] = initial_pos
    
    return y

y = init_model(total_time, initial_pos, initial_velocity)

def get_next_y(i, j, y, delta_t=delta_t, delta_x=delta_x, v=wave_speed,):
    '''
    Return y(x_i, t_j+1) based on data from surrounding and previous points in y.
    Boundary conditions: constant: y(x_i, t_i) = 0.
    '''
    k = (delta_t**2 * v**2)/(delta_x**2)
    if i == 0 or i == y.shape[0]-1: #boundary conditions
        return 0
    A = y[i+1, j] - 2*y[i, j] + y[i-1, j]
    B = 2*y[i, j] - y[i, j-1]
    return k * A + B

def gen_plot(model_state):
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    x = [range(model_state.shape[1])]
    y = [range(model_state.shape[0])]
    x, y = np.meshgrid(x, y)
    ax.plot_surface(x, y, model_state)
    ax.set_ylabel('distance along string')
    ax.set_xlabel('time (num. steps)')
    plt.show()

def run_sim(img_mode:str, total_time=total_time, initial_pos=initial_pos):
    #run
    for j in range(1, total_time-1):
        y[:,j+1] = [get_next_y(i, j, y) for i in range(len(initial_pos))]
    #gen plot
    if img_mode == 'graph':
        gen_plot(y)

if __name__ == '__main__':
    run_sim(img_mode='graph')