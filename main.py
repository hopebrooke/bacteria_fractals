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
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
from pygame_widgets.toggle import Toggle


PI = math.pi
folder = f'DATA_{datetime.datetime.now().strftime("%Y%m%d-%H%M%S")}'

# Generate Seed for replicable results
SEED = npr.randint(0,100)
SEED = 397944378
npr.seed(SEED) # only need to do it here (not for every agent move)

# Global dicts to hold widgets
buttons ={}
sliders = {}
slider_outputs = {}
toggles = {}

# Mapping from parameter names to display names
slider_labels = {
    "c_max": "Max Nutrients (Cₘₐₓ)",
    "d_c": "Diffusion Rate (Dc)",
    "time_step": "Time Step (Δt)",
    "num_agents": "No. Agents",
    "seed": "Random Seed",
    "r_max": "Max Reaction (rₘₐₓ)",
    "K_m": "M.M. Const (Kₘ)",
    "m_min": "Min Mass (mₘᵢₙ)",
    "delta_H": "Mass to Energy (ΔH)",
    "F_d": "Drag Force (F_d)",
    "mu": "Viscosity (μ)",
    "p": "Nutrient to Mass (p)",
    "density": "Agent Density (ρ)"
}


# Save the current frame if 'save pic' button pressed
def save_frame(screen, filename):
    if not os.path.exists(f"figures/{folder}"):
        os.makedirs(f"figures/{folder}")
    filename = f"figures/{folder}/{filename}"
    if not filename.endswith('.png'):
        filename += '.png'
    pygame.image.save(screen, filename)
    print(f"Saved frame to {filename}")
    

# Save the simulation data to json if 'save data' button pressed
def save_data(state, filename):
    if not os.path.exists(f"figures/{folder}"):
        os.makedirs(f"figures/{folder}")
    state.save_data(f"figures/{folder}/{filename}")    
    

# Update button text (eg. play -> pause)
def set_button_text(button, new_text):
    button.string = new_text
    button.text = button.font.render(button.string, True, button.textColour)
    button.textRect = button.text.get_rect()
    button.alignTextRect()
    
    
# Switch play/pause state
def play_pause(state):
    state.toggle_pause()
    set_button_text(buttons['play_pause'], "Play" if state.paused else "Pause")
    
    
# Reset simulation
def reset(state):
    # Update parameters if sliders have been changed
    for key in sliders:
        state.set_params(key, sliders[key].getValue())
    state.reset()
    global folder
    folder = f'DATA_{datetime.datetime.now().strftime("%Y%m%d-%H%M%S")}' # change folder    
    # Create output directory for GIFs
    if not os.path.exists(f"figures/{folder}"):
        os.makedirs(f"figures/{folder}")
    set_button_text(buttons['play_pause'], "Play" if state.paused else "Pause") # reset changes state to paused so update button
   

# Initialise Widgets
def init_widgets(screen,state):
    offset = state.grid_size * 2
    # Menu buttons
    buttons['play_pause']=Button(screen, offset+10, 10, 80, 30, text="Play" if state.paused else "Pause", onClick=lambda:play_pause(state), 
                                 inactiveColour=(21,122,110), hoverColour=(15, 87, 80), radius=12, textColour=(225,228,221), pressedColour=(9,52,48))
    buttons['restart']=Button(screen, offset+100, 10, 80, 30, text="Reset", onClick=lambda:reset(state), 
                              inactiveColour=(21,122,110), hoverColour=(15, 87, 80), radius=12, textColour=(225,228,221), pressedColour=(9,52,48))
    buttons['save_data']=Button(screen, offset+10, 50, 80, 30, text="Save Data", onClick=lambda:save_data(state, f"data_{state.iteration}.csv"), 
                                inactiveColour=(21,122,110), hoverColour=(15, 87, 80), radius=12, textColour=(225,228,221), pressedColour=(9,52,48))
    buttons['save_pic']=Button(screen, offset+100, 50, 80, 30, text="Save Img", onClick=lambda:save_frame(screen, f"img_{state.iteration}"), 
                               inactiveColour=(21,122,110), hoverColour=(15, 87, 80), radius=12, textColour=(225,228,221), pressedColour=(9,52,48))
    
    # Set values to help spacing of sliders/ text boxes etc.
    # Sliders:
    s_width = 80 # slider width
    s_height = 10 # slider height
    s_x_indent = offset +50 # slider x position indent
    s_y_indent = 120 # slider y position indent
    # Textboxes
    tb_width = 50 # text box width
    tb_height = 30 # text box height
    tb_x_indent = s_x_indent + 90 # text box x position indent
    tb_y_indent = s_y_indent - 15 # text box y position indent
    tb_fontsize = 20  # textbox font size
    # Spacing values:
    n = 0  # Number of parameters added
    spacing = 55 # Spacing between parameters
    
    width, height = screen.get_size()

    # Create sliders and text boxes for each parameter
    sliders['seed'] = Slider(screen, s_x_indent-10, s_y_indent+n*spacing, s_width, s_height, 
                             min=0, max=400000000, step=1, colour=(100,100,100), handleColour=(30,21,60), initial=state.seed)
    slider_outputs['seed'] = TextBox(screen,tb_x_indent-10, tb_y_indent+n*spacing, tb_width+50, tb_height, fontSize=tb_fontsize, 
                                     textColour=(30,21,60), borderThickness=0, colour=(225,228,221))
    slider_outputs['seed'].disable() 
    n += 1
    sliders['num_agents'] = Slider(screen, s_x_indent, s_y_indent+n*spacing, s_width, s_height, 
                                   min=1, max=50, step=1, colour=(100,100,100), handleColour=(30,21,60), initial=state.num_agents)
    slider_outputs['num_agents'] = TextBox(screen,tb_x_indent, tb_y_indent+n*spacing, tb_width, tb_height, fontSize=tb_fontsize, 
                                           textColour=(30,21,60), borderThickness=0, colour=(225,228,221))
    slider_outputs['num_agents'].disable() 
    n += 1
    sliders['time_step'] = Slider(screen, s_x_indent, s_y_indent+n*spacing, s_width, s_height, 
                                  min=1, max=5, step=1, colour=(100,100,100), handleColour=(30,21,60), initial=state.time_step)
    slider_outputs['time_step'] = TextBox(screen,tb_x_indent, tb_y_indent+n*spacing, tb_width, tb_height, fontSize=tb_fontsize, 
                                          textColour=(30,21,60), borderThickness=0, colour=(225,228,221))
    slider_outputs['time_step'].disable() 
    n += 1
    sliders['c_max'] = Slider(screen, s_x_indent, s_y_indent+n*spacing, s_width, s_height, 
                              min=0.5, max=5, step=0.5, colour=(100,100,100), handleColour=(30,21,60), initial=state.c_max)
    slider_outputs['c_max'] = TextBox(screen,tb_x_indent, tb_y_indent+n*spacing, tb_width, tb_height, fontSize=tb_fontsize, 
                                      textColour=(30,21,60), borderThickness=0, colour=(225,228,221))
    slider_outputs['c_max'].disable() 
    n += 1
    sliders['d_c'] = Slider(screen, s_x_indent, s_y_indent+n*spacing, s_width, s_height, 
                            min=0.01, max=0.1, step=0.01, colour=(100,100,100), handleColour=(30,21,60), initial=state.d_c)
    slider_outputs['d_c'] = TextBox(screen,tb_x_indent, tb_y_indent+n*spacing, tb_width, tb_height, fontSize=tb_fontsize, 
                                    textColour=(30,21,60), borderThickness=0, colour=(225,228,221))
    slider_outputs['d_c'].disable() 
    n += 1
    sliders['r_max'] = Slider(screen, s_x_indent, s_y_indent+n*spacing, s_width, s_height, 
                              min=0.01, max=0.1, step=0.01, colour=(100,100,100), handleColour=(30,21,60), initial=state.agent_params['r_max'])
    slider_outputs['r_max'] = TextBox(screen,tb_x_indent, tb_y_indent+n*spacing, tb_width, tb_height, fontSize=tb_fontsize, 
                                      textColour=(30,21,60), borderThickness=0, colour=(225,228,221))
    slider_outputs['r_max'].disable() 
    n += 1
    sliders['K_m'] = Slider(screen, s_x_indent, s_y_indent+n*spacing, s_width, s_height, 
                            min=0.1, max=1, step=0.01, colour=(100,100,100), handleColour=(30,21,60), initial=state.agent_params['K_m'])
    slider_outputs['K_m'] = TextBox(screen,tb_x_indent, tb_y_indent+n*spacing, tb_width, tb_height, fontSize=tb_fontsize, 
                                    textColour=(30,21,60), borderThickness=0, colour=(225,228,221))
    slider_outputs['K_m'].disable() 
    n += 1
    sliders['m_min'] = Slider(screen, s_x_indent, s_y_indent+n*spacing, s_width, s_height, 
                              min=0.5, max=5, step=0.5, colour=(100,100,100), handleColour=(30,21,60), initial=state.agent_params['m_min'])
    slider_outputs['m_min'] = TextBox(screen,tb_x_indent, tb_y_indent+n*spacing, tb_width, tb_height, fontSize=tb_fontsize, 
                                      textColour=(30,21,60), borderThickness=0, colour=(225,228,221))
    slider_outputs['m_min'].disable() 
    n += 1
    sliders['delta_H'] = Slider(screen, s_x_indent, s_y_indent+n*spacing, s_width, s_height, 
                                min=1, max=20, step=1, colour=(100,100,100), handleColour=(30,21,60), initial=state.agent_params['delta_H'])
    slider_outputs['delta_H'] = TextBox(screen,tb_x_indent, tb_y_indent+n*spacing, tb_width, tb_height, fontSize=tb_fontsize, 
                                        textColour=(30,21,60), borderThickness=0, colour=(225,228,221))
    slider_outputs['delta_H'].disable() 
    n += 1
    sliders['F_d'] = Slider(screen, s_x_indent, s_y_indent+n*spacing, s_width, s_height, 
                            min=0.2, max=1.5, step=0.1, colour=(100,100,100), handleColour=(30,21,60), initial=state.agent_params['F_d'])
    slider_outputs['F_d'] = TextBox(screen,tb_x_indent, tb_y_indent+n*spacing, tb_width, tb_height, fontSize=tb_fontsize, 
                                    textColour=(30,21,60), borderThickness=0, colour=(225,228,221))
    slider_outputs['F_d'].disable() 
    n += 1    
    sliders['mu'] = Slider(screen, s_x_indent, s_y_indent+n*spacing, s_width, s_height, 
                           min=0.5, max=2, step=0.1, colour=(100,100,100), handleColour=(30,21,60), initial=state.agent_params['mu'])
    slider_outputs['mu'] = TextBox(screen,tb_x_indent, tb_y_indent+n*spacing, tb_width, tb_height, fontSize=tb_fontsize, 
                                   textColour=(30,21,60), borderThickness=0, colour=(225,228,221))
    slider_outputs['mu'].disable() 
    n += 1
    sliders['p'] = Slider(screen, s_x_indent, s_y_indent+n*spacing, s_width, s_height, 
                          min=0.005, max=0.03, step=0.005, colour=(100,100,100), handleColour=(30,21,60), initial=state.agent_params['p'])
    slider_outputs['p'] = TextBox(screen,tb_x_indent, tb_y_indent+n*spacing, tb_width, tb_height, fontSize=tb_fontsize, 
                                  textColour=(30,21,60), borderThickness=0, colour=(225,228,221))
    slider_outputs['p'].disable() 
    n += 1
    sliders['density'] = Slider(screen, s_x_indent, s_y_indent+n*spacing, s_width, s_height, 
                                min=0.02, max=0.2, step=0.02, colour=(100,100,100), handleColour=(30,21,60), initial=state.agent_params['density'])
    slider_outputs['density'] = TextBox(screen,tb_x_indent, tb_y_indent+n*spacing, tb_width, tb_height, fontSize=tb_fontsize, 
                                        textColour=(30,21,60), borderThickness=0, colour=(225,228,221))
    slider_outputs['density'].disable() 
    n += 1    

    toggles['mode'] = Toggle(screen, offset+((width-offset)//2)+10, height-23, 20, 10, startOn=True, onColour=(100,100,100),offColour=(100,100,100), handleOffColour=(30,21,60), handleOnColour=(21,122,110))

    
    
# Draw the bacteria/nutrient grid on the screen
def draw_grid(screen, state):
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

    # Draw text labels
    midpoint = state.grid_size
    font = pygame.font.SysFont("Arial", 15)
    iter_label = font.render(f"Iterations: {state.iteration}", True, (255, 255, 255))
    screen.blit(iter_label, (midpoint +100, 10))
    agent_label = font.render(f"Agents: {len(state.petri.agents)}", True, (255, 255, 255))
    screen.blit(agent_label, (midpoint - 50, 10))
    seed_label = font.render(f"Seed: {state.seed}", True, (255, 255, 255))
    screen.blit(seed_label, (midpoint-220, 10))
   

# Draw the UI panel on the right side of the screen
def draw_ui(screen, state):
    width, height = screen.get_size()
    panel_width = width - state.grid_size*2
    offset = state.grid_size * 2
    screen.fill((225,228,221), rect=(offset, 0, panel_width, height)) # background
    
    # Draw all slider labels
    font = pygame.font.SysFont("Arial", 12)
    n = 0
    for key in slider_outputs:
        label_text = slider_labels.get(key, key)
        label = font.render(f'{label_text}: ', True, (30,21,60))
        screen.blit(label, (offset+10, 95+n*55))  
        n +=1      
    # Update all slider texts based on slider values
    for key in slider_outputs:
        if key != "seed" and key != "p":
            slider_outputs[key].setText(f"{sliders[key].getValue():.2f}")
        else:
            slider_outputs[key].setText(f"{sliders[key].getValue()}")

    # Calculate ABCDE values based on sliders
    m_min = sliders['m_min'].getValue()
    density = sliders['density'].getValue()
    F_d = sliders['F_d'].getValue()
    mu = sliders['mu'].getValue()
    r_max = sliders['r_max'].getValue()
    c_max = sliders['c_max'].getValue()
    K_m = sliders['K_m'].getValue()
    p = sliders['p'].getValue()
    delta_H = sliders['delta_H'].getValue()
    d_c = sliders['d_c'].getValue()
    min_r = math.sqrt((m_min/density)/math.pi)
    v_max = (F_d/(4*math.pi*mu*min_r))
    vals = {}
    vals['A'] = K_m/c_max
    vals['B'] = (r_max*min_r)/(c_max*v_max)
    vals['C'] = (min_r*p*r_max)/(v_max*density)
    vals['D'] = (d_c)/(min_r*v_max)
    vals['E'] = (F_d*min_r)/(m_min*delta_H)
    # Display ABCDE values
    i = 0
    label = font.render(f'Dimensionless Params:', True, (30,21,60))
    screen.blit(label, (offset+10, 100 + n*55 + i*30))  
    i += 1
    for key in vals:
        label = font.render(f'{key}:  {vals[key]:.2f}', True, (30,21,60))
        screen.blit(label, (offset+(panel_width//2 - 40), 100 + n*55 + i*30))  
        i +=1
    label = font.render('Gif mode:', True, (30,21,60))

    screen.blit(label, ((offset+45), height-25))




def main():

 
    # Nutrient Grid Parameters:
    GRID_SIZE = 512  # Square grid dimensions
    TIME_STEP = 1 # Stepwise diffusion rate per loop iteration
    C_MAX = 1.0 # Max nutrient val oon a given square
    D_C = 0.05 # rate of diffusion

    AGENT_PARAMS = {
        "r_max": 0.0498,
        "K_m": 0.25,
        "m_min": 1,
        "delta_H": 10,
        "F_d": 0.5,
        "mu": 0.8,
        "p": 0.02,
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

    max_iters = 300000     # Number of loop iterations for simulation
    max_agents = 30000
    num_agents = 50   # Initial cell count
    mode = 'gif'    # 'vis' for visualisation, 'gif' same but saves images.

    # Simulation state (holds all simulation data + petri dish + agents)
    sim = SimulationState(GRID_SIZE, AGENT_PARAMS, C_MAX, D_C, TIME_STEP, SEED, num_agents, max_iters)
    sim.paused = True

    # Create output directory for GIFs
    if not os.path.exists(f"figures/{folder}"):
        os.makedirs(f"figures/{folder}")

    # Start simulation
    pygame.init()
    panel_width = 210 # UI on right
    screen = pygame.display.set_mode((GRID_SIZE*2 + panel_width, GRID_SIZE*2))
    clock = pygame.time.Clock()
    running = True

    draw_interval = 200
    pic_interval = 1000
    
    # First screen
    screen.fill("black")
    init_widgets(screen, sim)
    draw_ui(screen, sim)
    draw_grid(screen, sim)
    pygame_widgets.update([])

    pygame.display.flip()

    # Set up rectangles so we dont always need to update everything
    panel_rect = pygame.Rect(GRID_SIZE*2, 0, panel_width, GRID_SIZE*2)
    grid_rect = pygame.Rect(0, 0, GRID_SIZE*2, GRID_SIZE*2)
    
    # Continue while there are iterations left and the simulation is running

    while sim.iteration < sim.max_iters and len(sim.petri.agents) < max_agents and running:
        # Check for events (quit, mouse click)
        events = pygame.event.get()
        pygame_widgets.update(events)
        for event in events:
            if event.type == pygame.QUIT:
                running = False
                break
            # Redraw if mouse is clicked
            if event.type == pygame.MOUSEBUTTONUP:
                draw_grid(screen, sim)
                draw_ui(screen, sim)
                pygame.display.update(grid_rect)
                if toggles['mode'].value == False:
                    mode = 'vis'
                else:
                    mode = 'gif'
        pygame.display.update(panel_rect)
        

        # Update if simulation is not paused
        if not sim.paused:
            sim.update() # update agents + grid
            # Update pygame display every 100 iterations
            if sim.iteration % (draw_interval)==0:
                draw_grid(screen, sim)
                pygame.display.update(grid_rect)

                # Save image every 500 iterations
                if mode == 'gif' and sim.iteration % (pic_interval)==0:
                    pygame.image.save(screen, f"figures/{folder}/frame_{sim.iteration}.png")
                    
        clock.tick(60)

    
    save_data(sim, f"data_{sim.iteration}.json")
    save_frame(screen, f"img_{sim.iteration}.png") 

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
