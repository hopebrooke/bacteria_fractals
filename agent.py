import math
import numpy.random as npr
import numpy as np

PI = math.pi

class Agent:
    def __init__(self, x, y, mass, petri, params):
        self.x = x
        self.y = y
        self.mass = mass
        self.petri = petri

        self.params = params
        self.r_max = params["r_max"]
        self.K_m = params["K_m"]
        self.m_min = params["m_min"]
        self.m_max = 2*self.m_min
        self.delta_H = params["delta_H"]
        self.F_d = params["F_d"]
        self.mu = params["mu"]
        self.p = params["p"]
        self.density = params["density"]

        self.size = mass / self.density
        self.radius = math.sqrt(self.size / PI)

        self.drag = 4 * PI * self.mu  
        self.velocity = (self.F_d / (self.drag * self.radius))

        self.theta = npr.uniform(0, 2 * PI)
        self.time_to_change = npr.poisson(10)



    def eat(self):
        nutrient_level = self.petri.get_nutrient_level(self.x, self.y)
        nutrients_taken = (self.r_max * nutrient_level) / (self.K_m + nutrient_level)
        
        self.mass += (self.p * nutrients_taken * self.size)
        self.petri.consume_nutrient(self.x, self.y, nutrients_taken)
        
        self.update_properties()


    def move(self):
        if self.m_min < self.mass < self.m_max: 
            if  self.time_to_change > 0:
                dx = round(self.velocity * math.cos(self.theta))
                dy = round(self.velocity * math.sin(self.theta)) 
                
                self.x = max(0, min(self.x + dx, self.petri.grid_size - 1))
                self.y = max(0, min(self.y + dy, self.petri.grid_size - 1))
                
                work_done = abs(self.F_d) * self.velocity
                self.mass -= (work_done / self.delta_H)
                self.update_properties()
                self.time_to_change -= 1
            else:
                self.theta = npr.uniform(0, 2 * PI)
                self.time_to_change = npr.poisson(10)


    def replicate(self):
        if self.mass >= self.m_max:
            # Pick a random direction from 8 possible directions (Moore neighborhood)
            dx, dy = npr.choice([-1, 0, 1]), npr.choice([-1, 0, 1])

            # Ensure at least one direction is nonzero (prevents no movement)
            while dx == 0 and dy == 0:
                dx, dy = npr.choice([-1, 0, 1]), npr.choice([-1, 0, 1])

            new_x = max(0, min(self.petri.grid_size - 1, self.x + dx))
            new_y = max(0, min(self.petri.grid_size - 1, self.y + dy))            
            
            new_agent = Agent(new_x, new_y, self.mass / 2, self.petri, self.params)
            self.mass /= 2
            self.update_properties()
            return new_agent
        return None

    def update_properties(self):
        self.size = self.mass / self.density
        self.radius = math.sqrt(self.size / PI)
        self.velocity = (self.F_d / (self.drag * self.radius))
