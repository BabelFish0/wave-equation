import numpy as np
import math
from typing import Callable

class Initializer:
    
    def gauss(self, x_size:int=1000, delta_x:float=0.5, width:float=25, shift:float=250, amplitude:float=1, velocity:list=[0]*1000) -> tuple:
        '''Initialize with a gaussian wave
        https://www.desmos.com/calculator/ogk6wf0kq5
        '''
        def calc_exponent(x, width=width, shift=shift):
            numerator = -(x-shift)**2
            denominator = width**2
            return numerator/denominator
        init_pos = [amplitude*math.e**calc_exponent(x*delta_x) for x in range(x_size)]
        init_vel = [-velocity[x]*pos*(2/width**2)*(shift-x*delta_x) for x, pos in enumerate(init_pos)]
        return init_pos, init_vel
        #fix amplitude

class Model:
    params = {}
    init_pos = []
    init_vel = []
    y = []
    e = 0

    def constBoundary(self, i:int) -> int:
        return 0

    def useCustomParams(self, delta_x:float, length:float, delta_t:float, total_frames:int, boundary_condition:Callable, wave_speed:list=None, mass_density:list=None, tension:list=None) -> None:
        if (mass_density and tension) and not wave_speed:
            wave_speed = [math.sqrt(tension[i]/mass_density[i]) for i in range(len(tension))]
        self.params = {
            'delta_x' : delta_x,
            'length' : length,
            'delta_t' : delta_t,
            'wave_speed' : wave_speed,
            'mass_density' : mass_density,
            'tension' : tension,
            'total_frames' : total_frames,
            'boundary_condition' : boundary_condition
        }

    def useDefaultParams(self) -> None:
        self.useCustomParams(0.5, 500, 1e-2, 500, self.constBoundary, tension=[100]*1000, mass_density=[1]*1000)
        if not (len(self.init_pos) or len(self.init_vel)):
            init = Initializer()
            self.init_pos, self.init_vel = init.gauss()

    def init_model(self) -> None:
        init_pos = self.init_pos
        self.y = np.zeros(shape=(len(init_pos), self.params['total_frames']))
        self.y[:, 0] = [init_pos[i] - self.params['delta_t']*self.init_vel[i] for i in range(len(init_pos))]
        self.y[:, 1] = init_pos
    
    def compute_y(self, i:int, j:int) -> float:
        v = self.params['wave_speed'][i]
        delta_t = self.params['delta_t']
        delta_x = self.params['delta_x']
        y = self.y
        k = (delta_t**2 * v**2)/(delta_x**2)
        if i == 0 or i == y.shape[0]-1: #boundary conditions
            return self.params['boundary_condition'](i)
        A = y[i+1, j] - 2*y[i, j] + y[i-1, j]
        B = 2*y[i, j] - y[i, j-1]
        return k * A + B
    
    def compute_timestep(self, j:int) -> None:
        x_size = int(self.params['length']/self.params['delta_x'])
        # self.k_e, self.p_e = self.compute_energy(j)
        self.y[:, j+1] = [self.compute_y(i, j) for i in range(x_size)]
        self.e = sum(self.energy(j))
    
    def get_all_x_positions(self) -> list:
        x_size, delta_x = int(self.params['length']/self.params['delta_x']), self.params['delta_x']
        return [i*delta_x for i in range(0, x_size)]
    
    def get_num_x_steps(self) -> int:
        return int(self.params['length']/self.params['delta_x'])
    
    def shift_timesteps(self, shift:int, axis=1) -> None:
        self.y = np.roll(self.y, shift, axis=1)
    
    def randomize_wave_speed(self, min_max:tuple=(5, 15), section_width:int=500, seed:int = 0) -> None:
        import random
        random.seed = seed #TODO: fix random seed
        wave_speed = []
        x_size = self.get_num_x_steps()
        for i in range(x_size//section_width):
            modifier = random.random()
            wave_speed += [min_max[0] + (min_max[1]-min_max[0])*modifier]*section_width
        self.params['wave_speed'] = wave_speed + [min_max[0] + (min_max[1]-min_max[0])*modifier]*(x_size%section_width)
    
    def ke(self, i:int, j:int) -> float:
        y = self.y
        delta_t = self.params['delta_t']
        delta_x = self.params['delta_x']
        rho = self.params['mass_density'][i]
        y_dot = (y[i, j] - y[i, j-1])/delta_t
        return 0.5 * rho * delta_x * y_dot**2

    def delta_l(self, j:int) -> float:
        x_size = self.get_num_x_steps()
        y = self.y
        delta_x = self.params['delta_x']
        current_length = sum([math.sqrt((y[i, j]-y[i-1, j])**2+delta_x**2) for i in range(1, x_size)])
        return current_length - self.params['length']
    
    def energy(self, j:int) -> float:
        x_size = self.get_num_x_steps()
        ke_at_each_x = [self.ke(i, j) for i in range(1, x_size)]
        pe = 0.5*self.params['tension'][0]*self.delta_l(j)**2
        return sum(ke_at_each_x), pe

    # def compute_power(self, i:int, j:int) -> float:
    #     y = self.y
    #     delta_t = self.params['delta_t']
    #     delta_x = self.params['delta_x']
    #     y_prime = (y[i, j] - y[i-1, j])/delta_x
    #     y_dot = (y[i, j] - y[i, j-1])/delta_t
    #     return y_prime * y_dot
    
    # def compute_energy(self, j:int) -> float:
    #     x_size = self.get_num_x_steps()
    #     ke_at_each_x = [self.compute_power(i, j) for i in range(1, x_size)]
    #     pe = self.compute_extension(j)**2
    #     return sum(ke_at_each_x), pe