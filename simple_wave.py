import matplotlib.pyplot as plt
import numpy as np
import math

delta_x = 0.01
delta_t = 0.001
wave_speed = 5
total_time = 10000
x_size = 100

def init_pos_bell(x_size, x_scaling):
    return [math.e**(-1*(((x-x_size/2)*x_scaling)**2)) for x in range(x_size)]

initial_pos = init_pos_bell(x_size, 0.1)
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

def get_next_y(i, j, delta_t=delta_t, delta_x=delta_x, v=wave_speed, y=y):
    '''
    Return y(x_i, t_j+1) based on data from surrounding and previous points in y.
    Boundary conditions: constant: y(x_i, t_i) = 0.
    '''
    j += 1 #adjust time indecies
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
    #print(x.shape(), y.shape(), model_state.shape())
    ax.plot_surface(x, y, model_state)
    plt.show()

#run
for j in range(0, total_time-1):
    y[:,j+1] = [get_next_y(i, j) for i in range(len(initial_pos))]

print(y)
gen_plot(y)