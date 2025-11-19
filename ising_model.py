import numpy as np
import copy

class ClassicIsing: 

    """
    Simulates a classic Ising model based on the Metropolis update rule.

    Parameters
        grid (Grid Object): The Grid object with topology 
        temperature (float): The temperature of the system
        ferromagnetivity (float): Coupling strength of magnetic moments.
        Mf_External (float): External magnetic field applied to the system
    """

    def __init__(self, grid, temperature, ferromagnetivity, Mf_External):

        self.grid = grid

        self.temperature = temperature
        self.ferromagnetivity = ferromagnetivity
        self.Boltzmann = 1.380649*10**-23 # J/K
        
        self.ExternalMagneticField = Mf_External

    ### overloaded methods ###

    def __str__(self):
        """String representation of the ClassicIsing object."""
        return print(self.grid)
    
    ### class methods ###

    def update(self, update_rule):

        """
        Updates grid based on an update_rule.

        Parameters
            update_rule (method): Takes in an update rule to change grid between time steps
        """

        # apply the update rule to every point in the grid
        # for i in range(self.grid.n_x):
        #     for j in range(self.grid.n_y):
        #         point = self.grid.getPoint(i, j)
        #         if point != None:
        #             update_rule(point)

        # # select a random point and apply the update rule to that point
        # rand_x = np.random.randint(0, self.grid.n_x)
        # rand_y = np.random.randint(0, self.grid.n_y)
        # point = self.grid.getPoint(rand_x, rand_y)
        # if point is not None:
        #     update_rule(point)

        # select NxN random points with a probability of 1/N^2 to apply the update rule to.

        N = self.grid.n_x * self.grid.n_y
        for _ in range(N):
            rand_x = np.random.randint(0, self.grid.n_x)
            rand_y = np.random.randint(0, self.grid.n_y)
            point = self.grid.getPoint(rand_x, rand_y)
            if point is not None:
                update_rule(point)
                
        if self.grid.record_history:
            self.grid.grid_history.append(copy.deepcopy(self.grid.grid))
            
    def outputSpins(self):
                
        """
        Outputs the current grid as a 2D array of spins. 

        Returns
            grid_spins (2D np.array): 2D array of spins representing the current grid state
        """

        grid_spins = np.zeros(self.grid.grid.shape)

        for i in range(grid_spins.shape[0]):
            for j in range(grid_spins.shape[1]):
                grid_spins[i, j] = self.grid.grid[i, j].spin
        return grid_spins
    
        

    def metropolis(self, point):
        """
        Takes in a grid point and alters its value based off the metropolis update rule. 
        The rule goes as follows:

        The Metropolis update rule randomly selects a spin, calculates the energy change from flipping it,
        and accepts the flip if it lowers the energy or with probability exp(-dE / T) otherwise.

        Parameters
            point (Classic Point Object): as a classical Ising model point with a spin
        """
        effective_field = self.effective_field(point.x, point.y, self.ferromagnetivity, self.ExternalMagneticField)
        # jason note: changed to <= from < to allow for zero energy changes to always flip
        if point.changeInEnergy(effective_field) <= 0:
            point.changeSpin(point.spin * -1)
        else:
            prob = np.exp(-point.changeInEnergy(effective_field) / (self.Boltzmann * self.temperature))
            rand = np.random.rand()
            if rand < prob:
                point.changeSpin(point.spin * -1)

    
    def magnetization(self):
        """
        Calculates the total magnetization of the grid.
        """
        
        total_magnetization = np.abs(np.sum(self.grid()) / (self.grid.n_x * self.grid.n_y))

        return total_magnetization
    

    def changeTemp(self, newTemp):
        self.temperature = newTemp 
    
    def effective_field(self, i, j, J=1.0, h=0.0):

        """
        Calculates the effect magnetic field on a given spin based off its neighbors. 
        Here we implement the Von Neumann Nearest neighbor interaction.

        Parameters:
            grid (np.array): 2D array representing the grid of spins
            i (int): x-coordinate of the spin
            j (int): y-coordinate of the spin
            J=1.0 (float): Coupling constant
            h=0.0 (float): External magnetic field
        """
        up = self.grid.getPoint(i, j+1)
        down = self.grid.getPoint(i, j-1)
        left = self.grid.getPoint(i-1, j)
        right = self.grid.getPoint(i+1, j)

        neighbors = [up, down, left, right]

        B_eff = np.sum([neighbor for neighbor in neighbors if neighbor is not None])

        B_eff *= J
        B_eff += h
        
        return B_eff

    def runSimulation(self, n_steps):

        """
        Runs the Ising model simulation for a given number of steps.

        Parameters:
            n_steps (int): Number of simulation steps to run
        """
        if n_steps <= 0:
            return
        for step in range(n_steps):
            self.update(self.metropolis)

    # def magnetization(self):
    #      n_x = self.grid.n_x
    #      n_y = self.grid.n_y
    #      mag = np.absolute(np.sum(self.outputSpins()))/(n_x*n_y)
    #      return mag 

    def resetSimulation(self):
        """
        Resets the grid.
        """
        self.grid.resetGrid()


class TransverseIsing:

    """
        Basic implementation of a Quantum Ising Model, more specifically the Transverse Ising model.
        The tranverse field ising model applies two sets of pauli matrices to the spins in the system. 
        The first set is a pauli X applied to each qubit individually. The second set of terms is a coupled pauli Z applied
        between each qubit. 


        H = sum(X)

        Parameters
            state_vector (array) - a vector of complex amplitudes representing our current state
            n (integer) - n number of qubits
            rand_int (boolean) - assigns random values or not to state vector
            load_history (array) - loads in a history of the state vector
    """

    def __init__(self, n, coupling_strength, term_strength, rand_init=False, load_history=None, load_state=None):
        
        self.n = n
        self.J = coupling_strength
        self.h = term_strength
        


        if load_state is not None:
            self.state_vector = load_state
        else:
            if rand_init:
                rand_amps = np.random.rand(2**n) + 1j * np.random.rand(2**n)
                norm = np.linalg.norm(rand_amps)
                self.state_vector = rand_amps / norm
            else:
                self.state_vector = np.zeros(2**n, dtype=complex)
                self.state_vector[0] = 1.0 + 0.0j 

        if load_history is not None:
            self.state_history = load_history
        else:
            self.state_history = [self.state_vector.copy()]

    def calculateStep(self):

        newState = np.zeros_like(self.state_vector, dtype=complex)


        #Coupling Terms

        z = [1, -1]  # maps bit 0 -> +1, bit 1 -> -1

        for idx, amp in enumerate(self.state_vector):
            total = 0
            #Applying Pauli Z to state vector 
            for i_qubit in range(self.n):

                j_qubit = (i_qubit + 1) % self.n

                bi = (idx >> i_qubit) & 1
                bj = (idx >> j_qubit) & 1
                total += -self.J * z[bi] * z[bj]
                
            newState[idx] += total * amp

        #Non-coupling Terms (Tranverse Effect)

        for idx, amp in enumerate(self.state_vector):

            #Applying Pauli X to state vector
            for i_qubit in range(self.n):
            
                flipped_bit = idx ^ (1 << i_qubit)

                newState[flipped_bit] += -self.h * amp

        return newState
    
    def eularUpdate(self, dt):

        #Eular Update

        self.state_vector += self.calculateStep()*dt*1j 

        self.state_vector /= np.linalg.norm(self.state_vector)

        self.state_history.append(self.state_vector.copy())


    def runSimulation(self, n_steps=1000, dt=.001):

        """
        Runs the Tranverse Field Ising model simulation for a given number of steps.

        Parameters:
            n_steps (int): Number of simulation steps to run
        """
        if n_steps <= 0:
            return
        for step in range(n_steps):
            self.eularUpdate(dt)

    def magnetization(self):
        
        z = np.array([1, -1])  # 0 -> +1, 1 -> -1
        Mz_total = 0

        for idx, amp in enumerate(self.state_vector):
            prob = np.abs(amp)**2  # probability of being in this basis state
            for i_qubit in range(self.n):
                bi = (idx >> i_qubit) & 1
                Mz_total += z[bi] * prob

        Mz = Mz_total / self.n

        return Mz






        



    
