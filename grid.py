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
    

#We will have a Hole, Mobius, Cylinder, and Torus
class HoleGrid(Grid):

    """

    Parameters:
        n_x (int): Number of grid points in the x direction
        n_y (int): Number of grid points in the y direction
        gridPointObject (Class): The class object representing a grid point
        random_init (bool): Whether to initialize the grid randomly
        random_seed (int): Seed for random number generation
        loadGrid (Grid): An existing Grid object to load from
        hole_grid (2D np.array): Optional custom hole grid configuration
        c_x (int): x-coordinate of the center of the hole (optional)
        c_y (int): y-coordinate of the center of the hole (optional)
    
    """





    def __init__(self, n_x, n_y, gridPointObject, random_init=True, random_seed=1, loadGrid=None, hole_grid=None, c_x = None, c_y = None):
        super().__init__(n_x, n_y, gridPointObject, random_init, random_seed, loadGrid)
        

        self.hole_grid = hole_grid
        self.c_x = c_x
        self.c_y = c_y

        self.hole_point = gridPointObject(x=c_x,y=c_y,spin=0)

        # --- Default hole ---
        if hole_grid is None:
            cx, cy = self.n_x // 2, self.n_y // 2
            size = 3 if self.n_x >= 3 and self.n_y >= 3 else 1
            half = size // 2

            x_slice = slice(max(0, cx - half), min(self.n_x, cx + half + 1))
            y_slice = slice(max(0, cy - half), min(self.n_y, cy + half + 1))
            self.grid[x_slice, y_slice] = self.hole_point

        # --- Custom hole pattern ---
        else:
            hole_h, hole_w = hole_grid.shape
            cx = self.n_x // 2 if c_x is None else c_x
            cy = self.n_y // 2 if c_y is None else c_y

            hx0 = max(0, cx - hole_h // 2)
            hy0 = max(0, cy - hole_w // 2)
            hx1 = min(self.n_x, hx0 + hole_h)
            hy1 = min(self.n_y, hy0 + hole_w)

            hole_slice_x = slice(0, hx1 - hx0)
            hole_slice_y = slice(0, hy1 - hy0)

            mask = hole_grid[hole_slice_x, hole_slice_y] != 0
            self.grid[hx0:hx1, hy0:hy1][mask] = self.hole_point


    def getPoint(self, x_pos, y_pos):
            """
            Returns None if (x_pos, y_pos) lies in the hole or out of bounds,
            otherwise returns the grid value.
            """
            if not (0 <= x_pos < self.n_x and 0 <= y_pos < self.n_y):
                return None

            value = self.grid[x_pos, y_pos]

            return None if value.spin == 0 else value
