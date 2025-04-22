import pygame
import math
import numpy.random as npr
from tqdm import tqdm
import matplotlib.pyplot as plt
import os
import datetime
from agent import Agent
from petri import Petri
from simstate import SimulationState

import pygame_widgets
from pygame_widgets.button import Button


PI = math.pi
FOLDER = f'DATA_{datetime.datetime.now().strftime("%Y%m%d-%H%M%S")}'

# Generate Seed for replicable results
SEED = npr.randint(0,1000000000)
SEED = 2246357572
npr.seed(SEED) # only need to do it here (not for every agent move)


def save_frame(screen, filename):
    # make folder if it doesn't exist
    if not os.path.exists(f"figures/{FOLDER}"):
        os.makedirs(f"figures/{FOLDER}")
    # Save the current frame as an image in that folder
    filename = f"figures/{FOLDER}/{filename}"
    if not filename.endswith('.png'):
        filename += '.png'
    pygame.image.save(screen, filename)
    print(f"Saved frame to {filename}")
    

def save_data(state, filename):
    # make folder if it doesn't exist
    if not os.path.exists(f"figures/{FOLDER}"):
        os.makedirs(f"figures/{FOLDER}")
    state.save_data(f"figures/{FOLDER}/{filename}")    
    
    
    
# Draws the UI elements on the screen
def draw_ui(screen, state):
    
    # Draw nutrient map
    for x in range(state.grid_size):
        for y in range(state.grid_size):
            percent_diff = 1 - state.petri.nutrient_grid[x, y]/state.petri.C_max
            pygame.draw.circle(screen, (79+int(146*percent_diff),53+int(175*percent_diff),155+int(66*(percent_diff))), (x * 2, y * 2), 1)
    
    # Draw agents
    for agent in state.petri.agents:
        if agent.imotile:
            colour = (0,0,0)
        else:
            colour = (229, 89, 52)
        pygame.draw.circle(screen, colour, (int(agent.x * 2), int(agent.y * 2)), 1)
        pygame.draw.circle(screen, (229, 89, 52), (int(agent.x * 2), int(agent.y * 2)), 1)
    
    # Draw UI buttons
    play_pause_button=Button(screen, 10, 10, 60, 30, text="Play" if state.paused else "Pause", onClick=lambda:state.toggle_pause(), inactiveColour=(0, 200, 0) if state.paused else (200, 200, 0), hoverColour=(0, 200, 0) if state.paused else (200, 200, 0))
    restart_button=Button(screen, 80, 10, 60, 30, text="Reset", onClick=lambda:state.reset(), inactiveColour=(200,0,0), hoverColour=(200,0,0))
    save_data_button=Button(screen, 150, 10, 80, 30, text="Save Data", onClick=lambda:save_data(state, f"data_{state.iteration}.csv"), inactiveColour=(100,100,200), hoverColour=(100,100,100))
    save_pic_button=Button(screen, 240, 10, 80, 30, text="Save Img", onClick=lambda:save_frame(screen, f"img_{state.iteration}"), inactiveColour=(100,0,200), hoverColour=(100,0,200))

    # Draw text labels
    font = pygame.font.SysFont("Arial", 10)
    iter_label = font.render(f"Iterations: {state.iteration}", True, (255, 255, 255))
    screen.blit(iter_label, (510, 10))
    agent_label = font.render(f"Agents: {len(state.petri.agents)}", True, (255, 255, 255))
    screen.blit(agent_label, (430, 10))
    seed_label = font.render(f"Seed: {SEED}", True, (255, 255, 255))
    screen.blit(seed_label, (330, 10))



def main():
 
    # Nutrient Grid Parameters:
    GRID_SIZE = 500  # Square grid dimensions
    TIME_STEP = 1 # Stepwise diffusion rate per loop iteration
    C_MAX = 1.0
    D_C = 0.0498

    AGENT_PARAMS = {
        "r_max": 0.0498,
        "K_m": 0.25,
        "m_min": 1,
        "delta_H": 10,
        "F_d": 0.5,
        "mu": 0.8,
        "p": 0.01,
        "density": 0.08,
    }
    
    # Paper values
    min_r = math.sqrt((AGENT_PARAMS["m_min"]/AGENT_PARAMS["density"])/math.pi)
    v_max = (AGENT_PARAMS["F_d"]/(4*math.pi*AGENT_PARAMS["mu"]*min_r))
    print(f'A: {AGENT_PARAMS["K_m"]/C_MAX}')
    print(f'B: {(AGENT_PARAMS["r_max"]*min_r)/(C_MAX*v_max)}')
    print(f'C: {(min_r*AGENT_PARAMS["p"]*AGENT_PARAMS["r_max"])/(v_max*AGENT_PARAMS["density"])}')
    print(f'D: {(D_C)/(min_r*v_max)}')
    print(f'E: {(AGENT_PARAMS["F_d"]*min_r)/(AGENT_PARAMS["m_min"]*AGENT_PARAMS["delta_H"])}')
    # Simulation Parameters:
    max_iters = 500000     # Number of loop iterations for simulation
    num_agents = 1   # Initial cell count
    mode = 'gif'    # 'vis' for visualisation, 'gif' same but saves images.

    # Simulation state (holds all simulation data + petri dish + agents)
    sim = SimulationState(GRID_SIZE, AGENT_PARAMS, C_MAX, D_C, TIME_STEP, num_agents, max_iters)

    # Create output directory for GIFs
    if mode == 'gif' and not os.path.exists(f"figures/{FOLDER}"):
        os.makedirs(f"figures/{FOLDER}")

    # Start simulation
    pygame.init()
    
    screen = pygame.display.set_mode((GRID_SIZE*2, GRID_SIZE*2))
    clock = pygame.time.Clock()
    running = True

    draw_interval = 100
    pic_interval = 1000
    
    # First screen
    draw_ui(screen, sim)
    pygame.display.flip()

    # Continue while there are iterations left and the simulation is running
    while sim.iteration < sim.max_iters and running:
        # Check for events (quit, mouse click)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type != pygame.MOUSEMOTION:
                # Update screen for every mouse click/ keyboard press etc.
                draw_ui(screen, sim)
                pygame_widgets.update(events)
                pygame.display.flip()

        # Update if simulation is not paused
        if not sim.paused:
            sim.update() # update agents + grid
            
            # Update pygame display every 100 iterations
            if sim.iteration % (draw_interval)==0:
                screen.fill("black")
                draw_ui(screen, sim)
                pygame_widgets.update(events)
                pygame.display.flip()
                
                # Save image every 500 iterations
                if mode == 'gif' and sim.iteration % (pic_interval)==0:
                    pygame.image.save(screen, f"figures/{FOLDER}/frame_{sim.iteration}.png")

        clock.tick(60)
    
    # Keep window open until manually closed
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.flip()
        clock.tick(60)
        
    pygame.quit()


if __name__ == "__main__":
    main()
