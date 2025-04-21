# Bacteria Fractal Simulation

Coursework for Bio-Inspired Computing COMP5400.


## Running Sim

`python3 main.py`

Play/Pause and reset buttons on simulation.

Can choose 'vis' or 'gif' mode in code - basically the same but gif mode also saves the screen every 1000 iterations.

All other parameters can be changed in the code - will eventually add buttons/sliders for changing them on the sim but don't know just yet which parameters we want adjustable.

Object oriented approach: SimState object is created which has attributes for simulation parameters, flags for paused/playing, methods to initiate the petri dish object, update the simulation (move eat replicate and then diffuse) etc. 

Petri class has nutrient/environment attributes, methods for diffusion, and also a list of agent objects contained in it. Agent objects have agent specific attributes like mass, density, etc, and methods to move, eat, replicate, etc.

The UI updating/functions are in main.
