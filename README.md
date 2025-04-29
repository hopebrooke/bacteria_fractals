# Bacteria Fractal Simulation

Coursework for Bio-Inspired Computing COMP5400.


## Running Sim

Run `python3 main.py` to open the software

Use the Play/Pause button to start/continue or pause the simulation. When running the screen is updated every 100 iterations.

Use the Reset button to reset the simulation loading any changes made to the parameters.

Use the Save Data button to save the current data of the simulation. This is stored in a JSON file in the simulation instance's respective folder. The data is stored in the form:
- Simulation Parameters: this stores grid size, C<sub>max</sub>, D<sub>C</sub>, time step, number of initial agents, current iteration, and seed.
- Agent Parameters: this stores r<sub>max</sub>, K<sub>m</sub>, m<sub>min</sub>, $\detla$H, F<sub>d</sub>, $\mu$, p, and density.
- Agents: this stores a list of all agents' coordinates and mass values

Use the Save Img button to save an image of the current state of the simulation to the simulation instance's respective folder

Use the labeled sliders to adjust parameters. These are bounded to appropriate values. Once you have selected your new values make sure to press reset to ensure the simulation is updated.

Use the toggle at the bottom of the screen to toggle gif mode on and off. If toggled on an image of the screen is taken every 1000 iterations into the simulation instance's respective folder.

## GIF Production

To create a GIF out of a simulation run open `python3 gif_creator.py` and change the folder variable to the folder for your selected run. 

Once that variable is changed run the code and it will output a gif into the gifs folder.

## Fractal Analysis

To perform fractal analysis on a given simulation open `fractal_analysis.ipynb` and change the FILE variable to the relative path to the JSON file that stores the data. This file can be found in the simulation instance's respective folder after pressing the Save Data button.

Once the appropriate changes have been made run the notebook. This will produces 2 values and 2 graph. the first value and graph is for box-counting analysis and the second is lacunarity.

## Code Structure

Object oriented approach: SimState object is created which has attributes for simulation parameters, flags for paused/playing, methods to initiate the petri dish object, update the simulation (move eat replicate and then diffuse) etc. 

Petri class has nutrient/environment attributes, methods for diffusion, and also a list of agent objects contained in it. Agent objects have agent specific attributes like mass, density, etc, and methods to move, eat, replicate, etc.

The UI updating/functions are in main.


