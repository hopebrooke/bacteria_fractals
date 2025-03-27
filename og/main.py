import pygame
import math
import numpy.random as npr
import matplotlib.pyplot as plt
from tqdm import tqdm

from agent import Agent
from petri import Petri


PI = math.pi


def main():
    
    # -----------  INITIALISE PARAMETERS ----------------
    # Nutrient Grid Parameters:
    grid_size = 1000  # Square grid dimensions
    time_step = 0.01 # Stepwise diffusion rate per loop iteration
    C_max = 2.0      # Maximum nutrient value on a given square
    D_c = 0.025      # Rate of diffusion
    
    # Agent Parameters:
    num_agents = 1   # Initial cell count
    r_max = 0.1      # Maximum reaction rate
    # TODO: combine m_min m_max and mass into a single parameter?
    m_min = 1        # Minimum cell mass before immotability
    m_max = 2*m_min        # Maximum cell mass before division
    mass = m_min   # Initial cell mass
    mu = 1           # Viscosity
    K_m = 0.5       # Michaelis-Menten constant
    F_d =  0.125       # Drag force
    delta_H = 4.0    # Proportion of mass converted to metabolic energy
    density = 0.04   # Density of the agent
    p = 0.0175 
    
    # Simulation Parameters:
    iters = 10000     # Number of loop iterations for simulation


    # ------------ INITIALISE NUTRIENT GRID AND AGENTS ----------------
    petri = Petri(grid_size, C_max, D_c, time_step)
    x, y = grid_size//2, grid_size//2
    for i in range(num_agents):
        agent = Agent(x=x, y=y, mass=mass, density=density, F_d=F_d, mu=mu, petri=petri, 
                      r_max=r_max, K_m=K_m, m_min=m_min, m_max=m_max, delta_H=delta_H, p=p)
        petri.add_agent(agent)
 
 
    # ---------------------- START SIMULATION ---------------------------------
    for i in tqdm(range(iters)):
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
    screen = pygame.display.set_mode((grid_size, grid_size))
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
