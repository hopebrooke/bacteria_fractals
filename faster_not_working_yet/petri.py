import numpy as np

class Petri:
    def __init__(self, grid_size, C_max, D_c, time_step, max_agents=10000):
        self.grid_size = grid_size
        self.C_max = C_max
        self.D_c = D_c
        self.time_step = time_step

        # Initialize the nutrient grid
        self.nutrient_grid = np.full((grid_size, grid_size), C_max)

        # Pre-allocated structured array for agents
        self.max_agents = max_agents
        self.agents = np.zeros(max_agents, dtype=[
            ('x', np.int32),
            ('y', np.int32),
            ('mass', np.float32),
            ('velocity', np.float32),
            ('theta', np.float32),
            ('time_to_change', np.int32),
            ('alive', np.bool_)
        ])
        self.num_agents = 0  # Track actual agent count

    def add_agent(self, x, y, mass, velocity, theta, time_to_change):
        if self.num_agents < self.max_agents:
            self.agents[self.num_agents] = (x, y, mass, velocity, theta, time_to_change, True)
            self.num_agents += 1

    def laplacian(grid):
        """Fast diffusion calculation using numba."""
        laplace_grid = (np.roll(grid, 1, axis=0) +
                        np.roll(grid, -1, axis=0) +
                        np.roll(grid, 1, axis=1) +
                        np.roll(grid, -1, axis=1) - 
                        4 * grid)
        return laplace_grid

    def diffuse(self):
        """Apply diffusion equation to the nutrient grid."""
        self.nutrient_grid += self.time_step * (self.D_c * Petri.laplacian(self.nutrient_grid))

    def consume_nutrient(self, x, y, amount):
        """Consume nutrients at a given location."""
        self.nutrient_grid[x, y] = max(0, self.nutrient_grid[x, y] - amount)

    def get_nutrient_level(self, x, y):
        """Get nutrient level at (x, y)."""
        return self.nutrient_grid[x, y]
