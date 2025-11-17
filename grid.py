import numpy as np
import copy 
class Grid:
    """
    Represents a 2D grid of points for the Ising model.

    Parameters
        n_x (int): Number of grid points in the x direction
        n_y (int): Number of grid points in the y direction
        gridPointObject (Class): The class object representing a grid point
        random_init (bool): Whether to initialize the grid randomly
        random_seed (int): Seed for random number generation
        loadGrid (Grid): An existing Grid object to load from
        record_history (bool): Whether to record the history of grid states over time
    """

    def __init__(self, n_x, n_y, gridPointObject, random_init=True, random_seed=None, loadGrid=None, record_history=True):

        
        self.gridPointObject = gridPointObject
        self.record_history = record_history
        self.loadGrid = loadGrid

        self.n_x = n_x
        self.n_y = n_y

        self.random_init = random_init
        self.random_seed = random_seed

        if self.random_seed is not None:
            np.random.seed(self.random_seed)

        if random_init:
            the_grid = self.initialize_grid()
            self.grid = the_grid
            if self.record_history:
                self.grid_history = [copy.deepcopy(the_grid)]
        else:
            self.grid = self.loadGrid
            if self.record_history:
                self.grid_history = self.loadGrid.grid_history

    ### overloaded methods ###

    def __call__(self):
        return self.grid

    def __str__(self):
        """String representation of the Grid object."""
        return str(self.output(self.grid))

    ### class methods ###

    def initialize_grid(self):
        spins = np.random.choice([-1, 1], size=(self.n_x, self.n_y))

        grid = np.empty((self.n_x, self.n_y), dtype=object)
        for i, j in np.ndindex(self.n_x, self.n_y):
            grid[i, j] = self.gridPointObject(i, j, spins[i, j])

        return grid

    def getPoint(self, x_pos, y_pos):

        """
        Here we define the getPoint method for the Grid class. This methods retrieves a requested point
        based off its coordinates. Different grid topologies might implement this differently and will override this method.
        The default version assumes a bounded square grid, meaning any points chosen outside the bound return None.

        Parameters
            point (Classic Point Object): as a classical Ising model point with a spin
        """

        if 0 <= x_pos < self.n_x and 0 <= y_pos < self.n_y:
            return self.grid[x_pos, y_pos]
        else:
            return None

    def output(self, grid):
        
        """
        Outputs the current grid as a 2D array of spins. 

        Returns
            grid_spins (2D np.array): 2D array of spins representing the current grid state
        """

        grid_spins = np.zeros(grid.shape)

        for i in range(grid_spins.shape[0]):
            for j in range(grid_spins.shape[1]):
                grid_spins[i, j] = grid[i, j].spin
        return grid_spins
    
    def resetGrid(self):
        """
        Resets the grid to a new random configuration if random_init is True. Else, returns the loaded grid. 
        """
        if self.random_init:
            self.grid = self.initialize_grid()
            if self.record_history:
                self.grid_history = [copy.deepcopy(self.grid)]
        else:
            self.grid = self.loadGrid.grid
            if self.record_history:
                self.grid_history = self.loadGrid.grid_history
        

#We will have a Hole, Möbius, Cylinder, and Torus
class HoleGrid(Grid):

    """
    Represents a 2D grid of points for the Ising model with a hole.

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
        super().__init__(n_x, n_y, gridPointObject, random_init, random_seed, loadGrid, record_history=True)
        

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
    
    def resetGrid(self):
        """Resets the grid to a new random initial configuration. Maintains the original hole structure."""
        if self.random_init:
            new_grid = self.initialize_grid()

            if self.hole_grid is None:
                cx, cy = self.n_x // 2, self.n_y // 2
                size = 3 if self.n_x >= 3 and self.n_y >= 3 else 1
                half = size // 2

                x_slice = slice(max(0, cx - half), min(self.n_x, cx + half + 1))
                y_slice = slice(max(0, cy - half), min(self.n_y, cy + half + 1))
                new_grid[x_slice, y_slice] = self.hole_point

            else:
                hole_h, hole_w = self.hole_grid.shape
                cx = self.n_x // 2 if self.c_x is None else self.c_x
                cy = self.n_y // 2 if self.c_y is None else self.c_y

                hx0 = max(0, cx - hole_h // 2)
                hy0 = max(0, cy - hole_w // 2)
                hx1 = min(self.n_x, hx0 + hole_h)
                hy1 = min(self.n_y, hy0 + hole_w)

                hole_slice_x = slice(0, hx1 - hx0)
                hole_slice_y = slice(0, hy1 - hy0)

                mask = self.hole_grid[hole_slice_x, hole_slice_y] != 0
                new_grid[hx0:hx1, hy0:hy1][mask] = self.hole_point

            self.grid = new_grid

            if self.record_history:
                self.grid_history = [copy.deepcopy(new_grid)]
        else:
            self.grid = self.loadGrid.grid
            if self.record_history:
                self.grid_history = self.loadGrid.grid_history


class Torus(Grid):
    """
    Represents a 2D grid of points for the Ising model with a torus topology.
    Parameters
        n_x (int): Number of grid points in the x direction
        n_y (int): Number of grid points in the y direction
        gridPointObject (Class): The class object representing a grid point
        random_init (bool): Whether to initialize the grid randomly
        random_seed (int): Seed for random number generation
        loadGrid (Grid): An existing Grid object to load from
    """

    def __init__(self, n_x, n_y, gridPointObject, random_init=True, random_seed=1, loadGrid=None):
        super().__init__(n_x, n_y, gridPointObject, random_init, random_seed, loadGrid)

    

    def getPoint(self, x_pos, y_pos):
        """
        Here we define the getPoint method for the Torus class. This methods retrieves a requested point
        based off its coordinates. The torus topology wraps around both edges.
        """

        x_wrapped = x_pos % self.n_x
        y_wrapped = y_pos % self.n_y

        return self.grid[x_wrapped, y_wrapped]
    
    def resetGrid(self):
        raise NotImplementedError("resetGrid method not implemented for Torus topology.")
    
class Cylinder(Grid):
    def __init__(self, n_x, n_y, gridPointObject, random_init=True, random_seed=1, loadGrid=None):
        super().__init__(n_x, n_y, gridPointObject, random_init, random_seed, loadGrid)

    

    def getPoint(self, x_pos, y_pos):
        """
        Here we define the getPoint method for the Cylinder class. This methods retrieves a requested point
        based off its coordinates. The cylinder topology wraps around the y edges but is bounded in the x direction.
        """

        if 0 <= x_pos < self.n_x:
            y_wrapped = y_pos % self.n_y
            return self.grid[x_pos, y_wrapped]
        else:
            return None
    
    def resetGrid(self):
        raise NotImplementedError("resetGrid method not implemented for Cylinder topology.")
        

class Mobius(Grid):
    """
    Represents a 2D grid of points for the Ising model with a Möbius strip topology.
    Parameters
        n_x (int): Number of grid points in the x direction
        n_y (int): Number of grid points in the y direction
        gridPointObject (Class): The class object representing a grid point
        random_init (bool): Whether to initialize the grid randomly
        random_seed (int): Seed for random number generation
        loadGrid (Grid): An existing Grid object to load from
    """

    def __init__(self, n_x, n_y, gridPointObject, random_init=True, random_seed=1, loadGrid=None):
        super().__init__(n_x, n_y, gridPointObject, random_init, random_seed, loadGrid)

    def getPoint(self, x_pos, y_pos):
        """
        Here we define the getPoint method for the Möbius class. This methods retrieves a requested point
        based off its coordinates. The Möbius topology wraps around the y edges with a twist and is bounded in the x direction.

        """

    def getPoint(self, x_pos, y_pos):
        """
        Return the point at (x_pos, y_pos) as if on a Möbius strip.
        The strip wraps around the y edges with a twist (mirror in x),
        and is bounded in the x direction.
        """

        if 0 <= x_pos < self.n_x:
            if y_pos < 0:
                y_wrapped = (y_pos % self.n_y)
                x_wrapped = (self.n_x - 1) - x_pos
            elif y_pos >= self.n_y:
                y_wrapped = (y_pos % self.n_y)
                x_wrapped = (self.n_x - 1) - x_pos
            else:
                y_wrapped = y_pos
                x_wrapped = x_pos

            return self.grid[x_wrapped, y_wrapped]
        else:
            return None
    
    def resetGrid(self):
        raise NotImplementedError("resetGrid method not implemented for Möbius topology.")

