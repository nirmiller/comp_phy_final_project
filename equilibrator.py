from ising_model import ClassicIsing
import numpy as np

def equilibrate_grid(grid, equil_tolerance=.9, mag_hist = False, J=1):
    """
    run the simulation until the grid equilibrates. That is, until the mean magnetization in the low temp regime
    stops changing significantly
    
    Parameters:
    -----------
    grid : Grid
        The grid to equilibrate
    tolerance : float
        The tolerance for equilibration. When the change in average magnetization over 5 steps is less than this value,
        the grid is considered equilibrated.
    mag_hist : bool
        If True, return the history of average magnetizations instead of just whether equilibrated.
    J : float
        The coupling constant for the Ising model.
    """

    max_steps = grid.n_x * grid.n_y * 5  # arbitrary large number of steps to prevent infinite loops

    temps = np.linspace(1, 1.2, 15)  # low temperature range for equilibration
    models = []

    # create a model for each temperature
    for T in temps:
        model = ClassicIsing(grid, temperature=T, ferromagnetivity=J, Mf_External=0)
        models.append(model)

    if mag_hist:
        total_hist = []

    # track average magnetizations by step
    is_equilibrated = False
    avg_mags_hist = []
    for step in range(max_steps):
        mags = []
        # step each model once and record magnetizations
        for model in models:
            model.runSimulation(1)
            mags.append(model.magnetization())
        avg_mags = np.mean(mags)
        if mag_hist:
            total_hist.append(avg_mags)
        avg_mags_hist.append(avg_mags)
        if step > 5:
            # check past 5 steps for equilibration by seeing if all magnitudes are greater than tolerance
            if np.all(np.mean(avg_mags_hist[-5:]) > equil_tolerance):
                is_equilibrated = True
                return total_hist if mag_hist else is_equilibrated
    return total_hist if mag_hist else is_equilibrated

def proper_equilibration(grid, equil_tolerance=.9, J=1):
    # equilibrate the grid first
    equilibrated = equilibrate_grid(grid, equil_tolerance=equil_tolerance, J=J)
    max_attempts = 10
    attempt = 0
    while not equilibrated:
        print("Reached maximum steps without equilibration. Resampling grid and trying again.")
        grid.resetGrid()
        equilibrated = equilibrate_grid(grid, tolerance=equil_tolerance, J=J)
        attempt += 1
        if attempt >= max_attempts:
            raise ValueError("Maximum equilibration attempts reached. Change equilibration tolerance.")
    return equilibrated