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

    def getPoint(self, point):

        """
        Here we define the getPoint method for the Grid class. This methods restrieves a requested point
        based off its coordinates. Different grid topologies might implement this differently and will overide this method.
        The default versian assumes a boudned square grid, meaning any points chosen outside the bound return None. 

        Parameters
            point (Classic Point Object): as a classical Ising model point with a spin
        """

        x_pos = point.x
        y_pos = point.y

        if 0 <= x_pos < self.n_x and 0 <= y_pos < self.n_y:
            return self.grid[x_pos, y_pos]
        else:
            return None

    def update_grid(self, update_rule):

        pass 

