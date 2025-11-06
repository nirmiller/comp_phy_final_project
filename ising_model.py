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
    
    def updateGrid(self, update_rule):

        """
        Updates grid based on an update_rule.

        Parameters
            update_rule (method): Takes in an update rule to change grid between timesteps
        """

        for i in range(self.grid.n_x):
            for j in range(self.grid.n_y):
                point = self.grid.getPoint(i, j)
                update_rule(point)

        self.grid.grid_history.append(self.grid.grid.copy())


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

        if point.changeInEnergy(self.effective_field(point.x, point.y, self.ferromagnetivity, self.ExternalMagneticField)) < 0:
            point.changeSpin(point.spin * -1)
        else:
            prob = np.exp(-point.changeInEnergy(self.effective_field(point.x, point.y, self.ferromagnetivity, self.ExternalMagneticField)) / (self.Boltzmann * self.temperature))
            rand = np.random.rand()
            if rand < prob:
                point.changeSpin(point.spin * -1)

    
    def magnetization(self):

        return 
    
    def effective_field(self, i, j, J=1.0, h=0.0):

        """
        Calculates the effect magnetic field on a given spin based off its neighbors. 
        Here we implement the Von Nuemenn Nearest neighrbor interaction.

        Parameters:
            grid (np.array): 2D array representing the grid of spins
            i (int): x-coordinate of the spin
            j (int): y-coordinate of the spin
            J=1.0 (float): Coupling constant
            h=0.0 (float): External magnetic field
        """

        B_eff = self.grid.grid.getPoint(i+1, j).spin + self.grid.grid.getPoint(i-1, j).spin + self.grid.grid.getPoint(i, j+1).spin + self.grid.grid.getPoint(i, j-1).spin
        B_eff *= J
        B_eff += h
        
        return B_eff


    
