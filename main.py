import pygame
import math
import numpy.random as npr
import matplotlib.pyplot as plt
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

from agent import Agent
from petri import Petri


PI = math.pi


def main():
    
    # -----------  INITIALISE CONST PARAMETERS ----------------
    # Nutrient Grid Parameters:
    GRID_SIZE = 1000  # Square grid dimensions
    TIME_STEP = 0.01 # Stepwise diffusion rate per loop iteration
    C_MAX = 2.0      # Maximum nutrient value on a given square
    D_C = 0.025      # Rate of diffusion
    
    # Agent Parameters:
    AGENT_PARAMS = {
        "r_max": 0.1,
        "K_m": 0.5,
        "m_min": 1,
        "m_max": 2,
        "delta_H": 4.0,
        "F_d": 0.125,
        "mu": 1,
        "drag": 4*PI*1, # 4 pi mu (saves recalculating loads)
        "p": 0.0175,
        "density": 0.04
    }
    # TODO: combine m_min m_max and mass into a single parameter?

    # Simulation Parameters:
    mass = AGENT_PARAMS["m_min"]   # Initial cell mass
    iters = 5000     # Number of loop iterations for simulation
    num_agents = 1   # Initial cell count

    # ------------ INITIALISE NUTRIENT GRID AND AGENTS ----------------
    petri = Petri(GRID_SIZE, C_MAX, D_C, TIME_STEP)

    x, y = GRID_SIZE//2, GRID_SIZE//2
    for _ in range(num_agents):
        agent = Agent(x=x, y=y, mass=mass, petri=petri, params=AGENT_PARAMS)
        petri.add_agent(agent)
 
    # ---------------------- START SIMULATION ---------------------------------
    for _ in tqdm(range(iters)):
        for agent in petri.agents:
            agent.move()
            agent.eat()
            new_agent = agent.replicate()
            if new_agent:
                petri.add_agent(new_agent)
        petri.diffuse()

    print(f'Num of agents: {len(petri.agents)}')


    # ---------------------- SHOW RESULTS ---------------------------------
    pygame.init()
    screen = pygame.display.set_mode((GRID_SIZE, GRID_SIZE))
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
        for agent in petri.agents:
            pygame.draw.circle(surface=screen, center=(agent.x, agent.y), radius=1.0, width=0, color="red")

        # flip() the display to put your work on screen
        pygame.display.flip()
        clock.tick(60)  # limits FPS to 60

    pygame.quit()
    
    
    
if __name__ == "__main__":
    main()
