import math
import numpy.random as npr
import numpy as np

PI = math.pi

class Agent:
    def __init__(self, x, y, mass, density, F_d, mu, petri, r_max, K_m, m_min, m_max, delta_H, p):
        self.x = x
        self.y = y
        self.mass = mass
        self.size = mass / density
        self.radius = math.sqrt(self.size / PI)
        self.velocity = F_d / (4 * PI * mu * self.radius)
        self.theta = npr.uniform(0, 2 * math.pi)
        self.time_to_change = npr.poisson(lam=10)
        self.petri = petri
        self.r_max = r_max
        self.K_m = K_m
        self.m_min = m_min
        self.m_max = m_max
        self.delta_H = delta_H
        self.F_d = F_d
        self.density = density
        self.mu = mu
        self.p = p


    def eat(self):
        nutrient_level = self.petri.get_nutrient_level(self.x, self.y)
        nutrients_taken = (self.r_max * nutrient_level) / (self.K_m + nutrient_level)
        
        self.mass += (self.size * self.p * nutrients_taken)
        self.petri.consume_nutrient(self.x, self.y, nutrients_taken)
        
        self._update_properties()


    def move(self):
        if self.m_min < self.mass < self.m_max and self.time_to_change > 0:
            dx = int(round(self.velocity * math.cos(self.theta))) * 2
            dy = int(round(self.velocity * math.sin(self.theta))) * 2
            
            self.x = max(0, min(self.petri.grid_size - 1, self.x + dx))
            self.y = max(0, min(self.petri.grid_size - 1, self.y + dy))
            
            self.mass -= abs(self.F_d) * self.velocity / self.delta_H
            self._update_properties()
            self.time_to_change -= 1
        else:
            self.theta = npr.uniform(0, 2 * math.pi)
            self.time_to_change = npr.poisson(lam=10)


    def replicate(self):
        if self.mass >= self.m_max:
            dx, dy = npr.choice([-1, 0, 1]), npr.choice([-1, 0, 1])
            while dx == 0 and dy == 0:
                dx, dy = npr.choice([-1, 0, 1]), npr.choice([-1, 0, 1])
                
            new_x = max(0, min(self.petri.grid_size - 1, self.x + dx))
            new_y = max(0, min(self.petri.grid_size - 1, self.y + dy))
            
            new_agent = Agent(new_x, new_y, self.mass / 2, self.density, self.F_d, self.mu, self.petri, 
                                self.r_max, self.K_m, self.m_min, self.m_max, self.delta_H, self.p)
            self.mass /= 2
            self._update_properties()
            return new_agent

    def _update_properties(self):
        self.size = self.mass / self.density
        self.radius = math.sqrt(self.size / PI)
        self.velocity = self.F_d / (4 * PI * self.mu * self.radius)
