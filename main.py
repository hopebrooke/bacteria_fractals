import pygame
import math
import numpy.random as npr
from tqdm import tqdm
import matplotlib.pyplot as plt
import os
import datetime
import random as rn

from agent import Agent
from petri import Petri



PI = math.pi

MODE = 'vis'  # Options: 'standard', 'gif', 'vis'
# 'standard' - only display at the end
# 'vis' - display frame every 1% of simulation
# 'gif' - same as vis but also saves image of frames every 1% GIF
FOLDER = f'{MODE}_{datetime.datetime.now().strftime("%Y%m%d-%H%M%S")}'

SEED = npr.uniform(0,1000000000)


def main():
    # -----------  INITIALISE CONST PARAMETERS ----------------
    # Nutrient Grid Parameters:
    GRID_SIZE = 500  # Square grid dimensions
    TIME_STEP = 0.01 # Stepwise diffusion rate per loop iteration
    C_MAX = 2.0      # Maximum nutrient value on a given square
    D_C = 0.025      # Rate of diffusion
    
    # Agent Parameters:
    AGENT_PARAMS = {
        "r_max": 0.1,    # maximum reaction rate
        "K_m": 0.5,      # michaelis menten constant
        "m_min": 5,      # minimum mass of agent
        "delta_H": 4.0,  # mass to energy rate
        "F_d": 0.125,    # drag force
        "mu": 0.75,      # viscosity
        "p": 0.0175,     # nutrient to mass rate
        "density": 0.4, # density of agent
        "seed": SEED
    }

    # Simulation Parameters:
    mass = AGENT_PARAMS["m_min"]   # Initial cell mass
    iters = 50000     # Number of loop iterations for simulation
    num_agents = 1   # Initial cell count

    # ------------ INITIALISE NUTRIENT GRID AND AGENTS ----------------
    petri = Petri(GRID_SIZE, C_MAX, D_C, TIME_STEP)

    x, y = GRID_SIZE//2, GRID_SIZE//2
    for _ in range(num_agents):
        agent = Agent(x=x, y=y, mass=mass, petri=petri, params=AGENT_PARAMS)
        petri.add_agent(agent)
 
    # ------------ CREATE OUTPUT DIRECTORY (for GIF mode) ------------
    if MODE == 'gif' and not os.path.exists(f"figures/{FOLDER}"):
        os.makedirs(f"figures/{FOLDER}")

    # ---------------------- START SIMULATION ---------------------------------
    # initialise pygame
    pygame.init()
    screen = pygame.display.set_mode((GRID_SIZE*2, GRID_SIZE*2))
    clock = pygame.time.Clock()
    running = True

    # start simulation loop
    for i in tqdm(range(iters)):
        for agent in petri.agents: # maybe parallelise this?
            agent.move()
            agent.eat()
            new_agent = agent.replicate()
            if new_agent:
                petri.add_agent(new_agent)
        petri.diffuse()

        # update pygame display ( every 1% for vis/gif, or just at end for standard)
        if ((MODE=='vis' or MODE=='gif') and i%(iters//100)==0) or (MODE=='standard' and i==iters-1):
            screen.fill("black")
            for x in range(0, GRID_SIZE):
                for y in range(0, GRID_SIZE):
                    pygame.draw.circle(surface=screen, center=(x*2, y*2), radius=1.0, width=0, color=pygame.Color(0,0,int(255*(petri.nutrient_grid[x, y]/2))))
            for agent in petri.agents:
                pygame.draw.circle(surface=screen, center=(agent.x*2, agent.y*2), radius=1.0, width=0, color="red")
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            if MODE == 'gif':
                pygame.image.save(screen, f"figures/{FOLDER}/frame_{i}.png")
            clock.tick(60)

        if not running:
            break
    
    # keep window open until manually closed
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.flip()

        clock.tick(60)
    pygame.quit()


if __name__ == "__main__":
    main()
