# Bacteria Fractal Simulation

Coursework for Bio-Inspired Computing COMP5400.


## Running Sim

To install required libraries:
```
pip install -r requirements.txt
```

To run the application:
```
python3 main.py
```

## Controls

- **Play/Pause Button:** Starts or pauses the simulation. When running the screen is updated every 100 iterations.
- **Reset Button:** Resets the simulation loading any changes made to the parameters.
- **Save Data Button:** Saves the current data of the simulation. This is stored in a JSON file in the simulation instance's respective folder. The data is stored in the form:
  - Simulation Parameters: Stores grid size, C<sub>max</sub>, D<sub>C</sub>, time step, number of initial agents, current iteration, and seed.
  - Agent Parameters: Stores r<sub>max</sub>, K<sub>m</sub>, m<sub>min</sub>, $\Delta$ H, F<sub>d</sub>, $\mu$, p, and density.
  - Agents: Stores a list of all agents' coordinates and mass values
- **Save Img Button:** Saves an image of the current state of the simulation to the simulation instance's respective folder
- **Labelled Sliders:** Adjusts simulation parameters. These are bounded to appropriate values. Once you have selected your new values press reset to ensure the simulation state is updated.
- **Mode Toggle:** Toggles gif mode on and off. When on, an image of the screen is taken every 1000 iterations into the simulation instance's respective folder.

## GIF Production

To create a GIF out of a simulation:

```python3 gif_creator.py <image_folder>```

The created gif will be saved in `gifs/`.

## Fractal Analysis

To perform fractal analysis on a given simulation open `fractal_analysis.ipynb` and set the `FILE` variable as the relative path to the saved data JSON file.

Run the notebook to perform box-counting and lacunarity.



