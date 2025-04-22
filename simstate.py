
from agent import Agent
from petri import Petri
import numpy.random as npr
import json


class SimulationState:
    def __init__(self, grid_size, agent_params, c_max, d_c, time_step, num_agents, max_iters):
        self.grid_size = grid_size
        self.agent_params = agent_params.copy()
        self.c_max = c_max
        self.d_c = d_c
        self.time_step = time_step
        self.num_agents = num_agents

        self.iteration = 0
        self.max_iters = max_iters
        self.paused = True
        self.running = True

        self._init_petri()

    # Initialize the Petri dish with agents
    def _init_petri(self):
        self.petri = Petri(self.grid_size, self.c_max, self.d_c, self.time_step)
        self.petri.agents = []
        center = self.grid_size // 2
        for _ in range(self.num_agents):
            agent = Agent(center+int(npr.uniform(-25,25)), center+int(npr.uniform(-25,25)), self.agent_params["m_min"], self.petri, self.agent_params)
            self.petri.add_agent(agent)
        self.iteration = 0

    # Start from beginning
    def reset(self):
        self._init_petri()
        self.paused = True

    # Toggle pause state
    def toggle_pause(self):
        self.paused = not self.paused
        
        
    # Make a step in the simulation
    def update(self):
        if self.paused:
            return
        for agent in self.petri.agents:
            agent.eat()
            if not agent.imotile:
                agent.move()
                new_agent = agent.replicate()
                if new_agent:
                    self.petri.add_agent(new_agent)
        self.petri.diffuse()
        self.iteration += 1

    # Not used yet, but will be used for changing simulation parameters
    def apply_param_change(self, key, value):
        if key in self.agent_params:
            self.agent_params[key] = value
        elif key == "d_c":
            self.d_c = value
            self.petri.D_C = value
        elif key == "time_step":
            self.time_step = value
            self.petri.time_step = value
        elif key == "num_agents":
            self.num_agents = value
        elif key == "c_max":
            self.c_max = value
        elif key == "iters":
            self.iters = value
        else: 
            print(f"Invalid parameter key: {key}")
            return
        # Start from beginning if parameters change
        self.reset()


    def save_data(self, filename):
        data = {
            "simulation_params": {
                "grid_size": self.grid_size,
                "c_max": self.c_max,
                "d_c": self.d_c,
                "time_step": self.time_step,
                "num_agents_initial": self.num_agents,
                "current_iteration": self.iteration,
            },
            "agent_params": self.agent_params,
            "agents": [
                {
                    "x": agent.x,
                    "y": agent.y,
                    "mass": agent.mass
                }
                for agent in self.petri.agents
            ]
        }   

        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

        