from ising_model import ClassicIsing
import electron
from grid import Grid, HoleGrid, Mobius, Cylinder, Torus
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.animation import FuncAnimation
from IPython.display import Video

def plot_spin_orient(grid, title='Spin Orientations'):
    """
    Plots a color map, indicating the spin orientation (up or down) of the grid.
    """
    cmap = mcolors.ListedColormap(['indigo', 'lightgray', 'gold']) # indigo = down, grey = neither, yellow = up
    plt.figure(figsize=(6, 6))
    bounds = [-1.5, -0.5, 0.5, 1.5] # need this for labelling the ticks
    norm = mcolors.BoundaryNorm(bounds, cmap.N)
    
    plt.imshow(grid, cmap=cmap)
    cbar = plt.colorbar(ticks=[-1, 0, 1])
    cbar.set_ticklabels(['down', 'neither', 'up'])
    cbar.ax.minorticks_off()
    plt.title(title)
    plt.tight_layout()
    plt.show()

def animate_ising(grid_object, grid_history, interval=50, title="Ising Model Evolution"):
    """
    Creates an animation of the Ising model evolution.
    
    Parameters:
        grid_object: Grid, HoleGrid, Mobius, Cylinder, or Torus
        grid_history: grid's evolution
        interval: time in milliseconds between frames
        title: title of the animation
    """
    fig, ax = plt.subplots(figsize=(6, 6))
    cmap = mcolors.ListedColormap(['indigo', 'lightgray', 'gold'])
    bounds = [-1.5, -0.5, 0.5, 1.5] # need this for labelling the ticks
    norm = mcolors.BoundaryNorm(bounds, cmap.N)
    
    # Get initial frame (through grid_object.output())
    initial_frame = grid_object.output(grid=grid_history[0])
    im = ax.imshow(initial_frame, cmap=cmap, norm=norm)
    
    # Make a legend
    cbar = plt.colorbar(im, ax=ax, ticks=[-1, 0, 1], shrink=0.8, aspect=20)
    cbar.set_ticklabels(['down', 'neither', 'up'])
    cbar.ax.minorticks_off()
    
    title_text = ax.set_title(f'{title}: Step 0')
    
    def update(frame):
        # Get each frame (through grid_object.output())
        updated_grid = grid_object.output(grid=grid_history[frame])
        im.set_array(updated_grid)
        title_text.set_text(f'{title}: Step {frame}')
        return [im, title_text]
    
    ani = FuncAnimation(fig, update, frames=len(grid_history), interval=interval, blit=True, repeat=True)
    
    plt.tight_layout()
    return ani