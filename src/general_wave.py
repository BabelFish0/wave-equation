import numpy as np
import math
from typing import Callable

class Model:
    params = {}
    init_pos = []
    init_vel = []
    y = []

    def constBoundary(self, i) -> int:
        return 0

    #add enforce() which runs boundary condition on its own

    def useCustomParams(self, delta_x:float, length:float, delta_t:float, wave_speed:float, total_frames:int, boundary_condition:Callable) -> None:
        self.params = {
            'delta_x' : delta_x,
            'length' : length,
            'delta_t' : delta_t,
            'wave_speed' : wave_speed,
            'total_frames' : total_frames,
            'boundary_condition' : boundary_condition
        }

    def useDefaultParams(self) -> None:
        self.useCustomParams(0.5, 500, 1e-2, [10]*1000, 500, self.constBoundary)
        if not (len(self.init_pos) or len(self.init_vel)):
            self.init_pos = [1*math.e**(-1*(((x-500)*1e-2)**2)) for x in range(1000)]
            self.init_vel = [0]*len(self.init_pos)

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
        self.y[:, j+1] = [self.compute_y(i, j) for i in range(x_size)]
    
    def get_all_x_positions(self) -> list:
        x_size, delta_x = int(self.params['length']/self.params['delta_x']), self.params['delta_x']
        return [i*delta_x for i in range(0, x_size)]
    
    def get_num_x_steps(self) -> int:
        return int(self.params['length']/self.params['delta_x'])
    
    def shift_timesteps(self, shift:int, axis=1) -> None:
        self.y = np.roll(self.y, shift, axis=1)
    
    def randomize_wave_speed(self, min_max:tuple=(5, 15), section_width:int=500, seed:int = 0) -> None:
        import random
        random.seed = seed
        wave_speed = []
        x_size = self.get_num_x_steps()
        for i in range(x_size//section_width):
            modifier = random.random()
            wave_speed += [min_max[0] + (min_max[1]-min_max[0])*modifier]*section_width
        self.params['wave_speed'] = wave_speed + [min_max[0] + (min_max[1]-min_max[0])*modifier]*(x_size%section_width)
