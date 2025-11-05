import numpy as np

class Grid:

    def __init__(self, n_x, n_y, gridPointObject, random_init=True, random_seed=1, loadGrid=None):

        np.random.seed(random_seed)

        self.gridPointObject = gridPointObject
        
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

        pass 

    def update_grid(self, update_rule):

        pass 

