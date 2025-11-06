import numpy as np


class ClassicIsing: 

    """
    Simulates a classic Ising model based on the Metropolis update rule.

    Parameters
        grid (Grid Object): The Grid object with topology 
        temperature (float): The temperature of the system
        ferromagnetivity (float): Coupling strength of magnetic moments. 
    """

    def __init__(self, grid, temperature, ferromagnetivity, Mf_External):

        self.grid = grid
        self.temperature = temperature
        self.ferromagnetivity = ferromagnetivity
        self.Boltzmann = 1.380649*(10**-23)


        self.ExternalMagneticField = Mf_External  
    
    def update(self, update_rule):

        """
        Updates grid based on an update_rule.

        Parameters
            update_rule (method): Takes in an update rule to change grid between timesteps
        """

        return
    
    def metropolis(self, point):

        """
        Takes in a grid point and alters its value based off the metropolis update rule. 
        The rule goes as follows:

        The Metropolis update rule randomly selects a spin, calculates the energy change from flipping it,
        and accepts the flip if it lowers the energy or with probability exp(-dE / T) otherwise.

        Parameters
            point (Classic Point Object): as a classical Ising model point with a spin
        """

        return 
    
    def magnetization(self):

        return 
    
    def effective_field(self, grid, i, j, J=1.0, h=0.0):
        
        return #B_eff

    def spin_energy(self, grid, i, j, J=1.0, h=0.0):
        s = grid[i,j]
        B_eff = self.effective_field(grid, i, j, J, h)
        return -s * B_eff
    
