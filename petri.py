import numpy as np
from scipy.ndimage import convolve

class Petri:
    def __init__(self, grid_size, C_max, D_c, time_step):
        self.grid_size = grid_size
        self.C_max = C_max
        self.D_c = D_c
        self.time_step = time_step
        self.agents = np.array([])

        self.nutrient_grid = np.full((grid_size, grid_size), C_max)

        self.laplacian_kernel = np.array([[0, 1, 0],
                                          [1, -4, 1],
                                          [0, 1, 0]])

    def laplacian(self):       
        return convolve(self.nutrient_grid, self.laplacian_kernel, mode="nearest", cval=0.0)

    def diffuse(self):
        self.nutrient_grid += self.time_step * (self.D_c * self.laplacian())

    def consume_nutrient(self, x, y, amount):
        self.nutrient_grid[x, y] = max(self.nutrient_grid[x, y] - amount, 0)

    def get_nutrient_level(self, x, y):
        return self.nutrient_grid[x, y]
    
    def add_agent(self, agent):
        self.agents = np.append(self.agents, agent)
