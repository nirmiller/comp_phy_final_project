import numpy as np

class Grid:

    def __init__(self, n_x, n_y, gridPointObject, random_init=True, random_seed=1, loadGrid=None):
        
        np.random.seed(random_seed)

        self.gridPointObject = gridPointObject

        self.n_x = n_x
        self.n_y = n_y

        if random_init:
            self.grid = self.initalize_grid()
            self.grid_history = []
        else:
            self.grid = loadGrid
            self.grid_history = loadGrid.grid_history

    def initalize_grid(self):
        spins = np.random.choice([-1, 1], size=(self.n_x, self.n_y))

        grid = np.empty((self.n_x, self.n_y), dtype=object)
        for i, j in np.ndindex(self.n_x, self.n_y):
            grid[i, j] = self.gridPointObject(i, j, spins[i, j])

        return grid

    def getPoint(self, x_pos, y_pos):

        """
        Here we define the getPoint method for the Grid class. This methods restrieves a requested point
        based off its coordinates. Different grid topologies might implement this differently and will overide this method.
        The default versian assumes a boudned square grid, meaning any points chosen outside the bound return None. 

        Parameters
            point (Classic Point Object): as a classical Ising model point with a spin
        """

        if 0 <= x_pos < self.n_x and 0 <= y_pos < self.n_y:
            return self.grid[x_pos, y_pos]
        else:
            return None

    def output(self):
        
        """
        Outputs the current grid as a 2D array of spins. 

        Returns
            grid_spins (2D np.array): 2D array of spins representing the current grid state
        """

        grid_spins = np.zeros((self.n_x, self.n_y))

        for i in range(self.n_x):
            for j in range(self.n_y):
                grid_spins[i, j] = self.grid[i, j].spin

        return grid_spins