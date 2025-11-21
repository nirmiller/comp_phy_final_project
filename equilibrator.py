import copy
import numpy as np

def equilibrate_grid(model, equil_tolerance=.9, mag_hist = False):
    """
    Run the simulation until the grid equilibrates. That is, until the average magnetization of temps 
    between 1 and 1.2, is greater than the tolerance for 5 consecutive equilibrations.
    
    Parameters:
    -----------
    model : the ising model object
        The Ising model to equilibrate.
    tolerance : float
        The tolerance for equilibration. When the change in average magnetization over 5 steps is less than this value,
        the grid is considered equilibrated.
    mag_hist : bool
        If True, return the history of average magnetizations instead of just whether equilibrated.

    Returns:
    --------
    bool or list
        If mag_hist is False, returns True if the grid is equilibrated, False otherwise.
        If mag_hist is True, returns a list of average magnetizations at each step.
    """

    grid = model.grid
    max_steps = grid.n_x * grid.n_y * 5  # arbitrary large number of steps to prevent infinite loops
    temps = np.linspace(1, 1.2, 15)  # low temperature range for equilibration
    ensemble = []

    # create a new model for each temperature
    for T in temps:
        modelCopy = copy.deepcopy(model)
        modelCopy.grid = grid  # share the same grid
        new_model = modelCopy.changeTemp(T)
        ensemble.append(new_model)

    # create equilibration history list if desired.
    if mag_hist:
        total_hist = []

    # track average magnetizations by step
    is_equilibrated = False
    avg_mags_hist = []
    for step in range(max_steps):
        mags = []
        # step each model once and record magnetizations
        for sample in ensemble:
            sample.runSimulation(1)
            mags.append(sample.magnetization())
        avg_mags = np.mean(mags)

        if mag_hist:
            total_hist.append(avg_mags)

        avg_mags_hist.append(avg_mags)
        if step > 5:
            # check past 5 steps for equilibration by seeing if all magnitudes are greater than tolerance
            if np.all(np.mean(avg_mags_hist[-5:]) > equil_tolerance):
                is_equilibrated = True
                # equilibrated
                return total_hist if mag_hist else is_equilibrated
            
    # not equilibrated within max steps       
    return total_hist if mag_hist else is_equilibrated

def proper_equilibration(model, equil_tolerance=.9, max_attempts=10):
    """
    Calls equilibrate_grid, if still not equilibrated, resets/resamples the grid and tries again, up to a maximum number of attempts.

    Parameters:
    -----------
    model : the ising model object
        The Ising model to equilibrate.
    equil_tolerance : float
        The tolerance for equilibration.
    J : float
        The coupling constant for the Ising model.
    max_attempts : int
        The maximum number of attempts to equilibrate the grid.

    Returns:
    --------
    bool
        Returns True if the grid is equilibrated, False otherwise.
    """
    # equilibrate the grid first
    equilibrated = equilibrate_grid(model, equil_tolerance=equil_tolerance)
    attempt = 0
    # if not equilibrated, reset and try again
    while not equilibrated:
        model.resetSimulation()
        equilibrated = equilibrate_grid(model, equil_tolerance=equil_tolerance)
        attempt += 1
        if attempt >= max_attempts:
            print("Maximum attempts for proper equilibration reached. Equilibration is not ensured.")
            return equilibrated
    return equilibrated