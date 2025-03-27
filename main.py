import pygame
import math
import numpy.random as npr
import matplotlib.pyplot as plt
from tqdm import tqdm
import numpy as np


# pygame setup


PI = math.pi

grid_size = 500  # Square grid dimensions
time_step = 0.01 # Stepwise diffusion rate per loop iteration
iters = 1000  # Number of loop iterations for simulation
num_agents = 1   # Initial cell count
C_max = 2.0      # Maximum nutrient value on a given square
r_max = 0.1      # Maximum reaction rate
m_max = 2        # Maximum cell mass before division
m_min = 1        # Minimum cell mass before immotability
mu = 1           # Viscosity
D_c = 0.025      # Rate of diffusion
K_m = 0.5       # Michaelis-Menten constant
F_d =  0.125       # Drag force
delta_H = 4.0    # Proportion of mass converted to metabolic energy
density = 0.04   # Density of the agent
p = 0.0175 


# Initialise a grid with uniform nutrient distribution
nutrient_grid = np.full((grid_size*2, grid_size*2), C_max)
# Initialise a list for agents
agents = []

class Agent:
    def __init__(self, x=npr.randint(0, grid_size-1), y=npr.randint(0, grid_size-1), mass = m_min):
        self.x = x
        self.y = y
        self.mass = mass
        self.size = mass / density
        self.radius = math.sqrt(self.size / PI)
        self.velocity = F_d / (4 * PI * mu * self.radius)
        self.theta = npr.uniform(0, 2 * math.pi)
        self.time_to_change = npr.poisson(lam=10)  # λ = 10 from the Poisson distribution

    def eat(self):
      # Equation 5
      nutrients_taken = (r_max * nutrient_grid[self.x, self.y]) / (K_m + nutrient_grid[self.x, self.y])
      #print(f'Nutrients taken: {nutrients_taken}')
      # Nutrients to mass
      #print(f'{self.size * p * nutrients_taken}')
      #print(f'Mass of agent before eating: {self.mass}')
      self.mass += (self.size * p * nutrients_taken)
      #print(f'Mass gained: {self.size * p * nutrients_taken}')
      #print(f'Mass of agent after eating: {self.mass}')
      self.size = self.mass / density
      self.radius = math.sqrt(self.size / PI)
      self.velocity = F_d / (4 * PI * mu * self.radius)
      # Take away nutrients from the grid
      nutrient_grid[self.x, self.y] -= nutrients_taken


    def move(self):
      if self.mass > m_min and self.mass < m_max:
            # Move only if time_to_change is positive
            if self.time_to_change > 0:
                dx = int(round(self.velocity * math.cos(self.theta)))*2
                dy = int(round(self.velocity * math.sin(self.theta)))*2
                self.x = max(0, min(grid_size - 1, self.x + dx))
                self.y = max(0, min(grid_size - 1, self.y + dy))
                #print(f'Mass of agent before movement: {self.mass}')
                self.mass -= (abs(F_d) * self.velocity / delta_H) #(1/math.sqrt(1+self.mass)) * e(F_d, R_min, m_min, delta_H) #0.1 * (abs(F_d) * self.velocity / delta_H) #(self.size * delta_H * self.velocity)
                #print(f'Mass lost: {(abs(F_d) * self.velocity / delta_H)}')
                #print(f'Mass of agent after movement: {self.mass}')
                self.size = self.mass / density
                self.radius = math.sqrt(abs(self.size) / PI)
                self.velocity = F_d / (4 * PI * mu * self.radius)
                self.time_to_change -= 1

            else:
                # Change direction and reset Poisson-distributed persistence time
                self.theta = npr.uniform(0, 2 * math.pi)
                self.time_to_change = npr.poisson(lam=10)

    def replicate(self):
      if self.mass >= m_max:
          # Pick a random direction from 8 possible directions (Moore neighborhood)
          dx, dy = npr.choice([-1, 0, 1]), npr.choice([-1, 0, 1])

          # Ensure at least one direction is nonzero (prevents no movement)
          while dx == 0 and dy == 0:
              dx, dy = npr.choice([-1, 0, 1]), npr.choice([-1, 0, 1])

          new_x = max(0, min(grid_size - 1, self.x + dx))
          new_y = max(0, min(grid_size - 1, self.y + dy))
          agent = Agent(x=new_x, y=new_y, mass=(self.mass/2))
          agents.append(agent)
          self.mass /= 2
          self.size = self.mass / density
          self.radius = math.sqrt(self.size / PI)
          self.velocity = F_d / (4 * PI * mu * self.radius)
          self.theta = npr.uniform(0, 2 * math.pi)
          self.time_to_change = npr.poisson(lam=10)  # λ = 10 from the Poisson distribution

def laplacian(nutrient_grid):
    lap = (np.roll(nutrient_grid, 1, axis=0) + np.roll(nutrient_grid, -1, axis=0) +
           np.roll(nutrient_grid, 1, axis=1) + np.roll(nutrient_grid, -1, axis=1) - 4 * nutrient_grid)
    return lap

def diffusion(nutrient_grid):
    # D_c is the rate of diffusion
    nutrient_grid += time_step * (D_c * laplacian(nutrient_grid))
    #for agent in agents:
    #    nutrient_grid[agent.x, agent.y] -= (r_max * nutrient_grid[agent.x, agent.y]) / (K_m + nutrient_grid[agent.x, agent.y])

for agent in range(num_agents):
    agent = Agent(x=500, y=500)
    agents.append(agent)

current_iter = 0

for i in tqdm(range(iters)):
    for agent in agents:
        agent.move()
        agent.eat()
        agent.replicate()
    diffusion(nutrient_grid=nutrient_grid)

print(len(agents))
for agent in agents:
    print(f'{agent.x}, {agent.y}')

plt.figure(figsize=(8, 8))
x_vals = [agent.x for agent in agents]
y_vals = [agent.y for agent in agents]
#plt.xlim(0, grid_size)
#plt.ylim(0, grid_size)
plt.scatter(
    [agent.x for agent in agents],
    [agent.y for agent in agents],
    s=1, c='blue', alpha=0.6
)
plt.title("Bacteria-Inspired Fractal Growth")
plt.show()

pygame.init()
screen = pygame.display.set_mode((grid_size*2, grid_size*2))
clock = pygame.time.Clock()
running = True

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")


    # RENDER YOUR GAME HERE

    for agent in agents:
        pygame.draw.circle(surface=screen, center=(agent.x, agent.y), radius=1.0, width=0, color="red")


    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()