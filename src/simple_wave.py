import pos_vel_init as pv_init
import matplotlib.pyplot as plt
import numpy as np
import math

def init_pos_bell(x_size, x_scaling, y_scaling):
    '''A possible starting shape'''
    return [y_scaling*math.e**(-1*(((x-x_size/2)*x_scaling)**2)) for x in range(x_size)]

def init_model(total_time, initial_pos, initial_velocity, delta_t):
    '''
    Return an initialised array of correct shape with first
    two timesteps (t=-1 and t=0 which are stored as t0 and t1)
    adequately filled for normal calculation.
    '''
    if len(initial_pos) != len(initial_velocity):
        print('oops, len(initial_pos) != len(initial_velocity)')
        return
    
    y = np.zeros(shape=(len(initial_pos), total_time), dtype=np.float64) #shape = (num x points, num t steps), array initialised for num t_steps that will be stored

    y[:, 0] = [initial_pos[i] - delta_t*initial_velocity[i] for i in range(len(initial_pos))]
    y[:, 1] = initial_pos
    
    return y

def get_next_y(i, j, y, delta_t, delta_x, v):
    '''
    Return y(x_i, t_j+1) based on data from surrounding and previous points in y.
    Boundary conditions: constant: y(x_i, t_i) = 0.
    '''
    k = (delta_t**2 * v**2)/(delta_x**2)
    if i == 0 or i == y.shape[0]-1: #boundary conditions
        return 0
    A = y[i+1, j] - 2*y[i, j] + y[i-1, j]
    B = 2*y[i, j] - y[i, j-1]
    return k * A + B #rearranged PDE for y(x_i, t_{j+1}) ie the solution for displacement at same pos, next time

def gen_plot(model_state):
    '''
    Generate full plot of position against time against vertical displacement.
    '''
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    x = [range(model_state.shape[1])]#times ie {0, 1, 2 ... total_time} where the number represents the num timesteps
    y = [range(model_state.shape[0])]#positions across the line
    x, y = np.meshgrid(x, y)
    ax.plot_surface(x, y, model_state)#model_state (ie y(x, t)) contains all the vertical displacements of points on the wave for a given time and position.
    ax.set_ylabel('distance along string')
    ax.set_xlabel('time (num. steps)')
    plt.show()

def run_sim(y, img_mode:str, total_time, initial_pos, delta_t, delta_x, wave_speed):
    '''
    Standard run parameters for saving all timesteps (not used by animator).
    '''
    #run
    for j in range(1, total_time-1):
        y[:,j+1] = [get_next_y(i, j, y, delta_t, delta_x, wave_speed) for i in range(len(initial_pos))]
    #gen plot
    if img_mode == 'graph':
        gen_plot(y)

if __name__ == '__main__':
    '''
    Default output if not imported as a module..

    '''
    #general parameters
    delta_x = 0.5
    delta_t = 1e-2
    wave_speed = 10
    total_time = 2000*4
    x_size = 1000

    # initial_pos = init_pos_bell(x_size, 0.01, 1) #function for initial shape of curve
    # initial_velocity = [0]*x_size #initial velocities of points on the wave

    initial_pos, initial_velocity, y_min, y_max = pv_init.bell_at_rest(x_size, 0.01, 1) #updated standard init func

    y = init_model(total_time, initial_pos, initial_velocity, delta_t) #set up array and create first two timesteps so normal algorithm works
    run_sim(y, delta_t=delta_t, delta_x=delta_x, wave_speed=wave_speed, img_mode='graph', total_time=1000*8, initial_pos=initial_pos) #run next timesteps with parameters