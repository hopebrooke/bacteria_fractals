import math
import numpy.random as npr
import numpy as np

PI = math.pi

class Agent:
    def __init__(self, petri, r_max, K_m, m_min, m_max, delta_H, p, density, F_d, mu):
        self.petri = petri
        self.r_max = r_max
        self.K_m = K_m
        self.m_min = m_min
        self.m_max = m_max
        self.delta_H = delta_H
        self.p = p
        self.density = density
        self.F_d = F_d
        self.mu = mu

    def initialize_agents(self, num_agents):
        """Vectorized initialization of agents at the center of the Petri dish."""
        center_x, center_y = self.petri.grid_size // 2, self.petri.grid_size // 2
        mass = self.m_min
        velocity = self.calculate_velocity(mass)
        theta = npr.uniform(0, 2 * math.pi, num_agents)
        time_to_change = npr.poisson(lam=10, size=num_agents)

        for i in range(num_agents):
            self.petri.add_agent(center_x, center_y, mass, velocity, theta[i], time_to_change[i])

    def calculate_velocity(self, mass):
        """Calculate velocity based on mass and physical properties."""
        size = mass / self.density
        radius = math.sqrt(size / PI)
        return self.F_d / (4 * PI * self.mu * radius)

    def update_agents(self):
        """Vectorized update of all agents."""
        agents = self.petri.agents[:self.petri.num_agents]  # Only consider active agents

        # Move only alive agents
        moving_agents = agents#[agents['alive']]
        moving_agents['x'] += np.round(moving_agents['velocity'] * np.cos(moving_agents['theta'])).astype(np.int32)
        moving_agents['y'] += np.round(moving_agents['velocity'] * np.sin(moving_agents['theta'])).astype(np.int32)

        # Keep agents within bounds
        moving_agents['x'] = np.clip(moving_agents['x'], 0, self.petri.grid_size - 1)
        moving_agents['y'] = np.clip(moving_agents['y'], 0, self.petri.grid_size - 1)

        # Decrease mass slightly due to movement
        moving_agents['mass'] -= np.abs(self.F_d) * moving_agents['velocity'] / self.delta_H

        # Agents with too low mass become immobile (set `alive` to False)
        #agents['alive'] = agents['mass'] > self.m_min

    def eat(self):
        """Vectorized nutrient consumption."""
        agents = self.petri.agents[:self.petri.num_agents]
        x, y = agents['x'], agents['y']

        nutrient_levels = self.petri.nutrient_grid[x, y]
        nutrients_taken = (self.r_max * nutrient_levels) / (self.K_m + nutrient_levels)

        # Update mass based on nutrient intake
        agents['mass'] += (agents['mass'] * self.p * nutrients_taken)

        # Reduce nutrients in grid
        self.petri.nutrient_grid[x, y] = np.maximum(0, self.petri.nutrient_grid[x, y] - nutrients_taken)

    def replicate(self):
        """Vectorized replication process."""
        agents = self.petri.agents[:self.petri.num_agents]

        # Find agents ready to divide
        dividing_agents = agents[agents['mass'] >= self.m_max]

        # Determine random movement direction
        dx = npr.choice([-1, 0, 1], size=len(dividing_agents))
        dy = npr.choice([-1, 0, 1], size=len(dividing_agents))

        # Ensure they move
        zero_moves = (dx == 0) & (dy == 0)
        dx[zero_moves] = 1  # Assign movement if necessary

        # Calculate new agent positions
        new_x = np.clip(dividing_agents['x'] + dx, 0, self.petri.grid_size - 1)
        new_y = np.clip(dividing_agents['y'] + dy, 0, self.petri.grid_size - 1)

        # Half mass
        dividing_agents['mass'] /= 2

        # Add new agents
        for i in range(len(dividing_agents)):
            self.petri.add_agent(new_x[i], new_y[i], dividing_agents['mass'][i],
                                 self.calculate_velocity(dividing_agents['mass'][i]),
                                 npr.uniform(0, 2 * np.pi), npr.poisson(10))
