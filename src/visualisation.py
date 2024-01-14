import matplotlib.lines
import mpl_toolkits.mplot3d as p3
import mpl_toolkits.mplot3d.art3d
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from typing import List, Union
from random_walker import RandomWalker
from typing import Tuple
import os

matplotlib.use("TkAgg")


def setup_axes(ndim: int) -> Tuple[plt.Figure, Union[plt.Axes, p3.axes3d.Axes3D]]:
    """
    Set up the matplotlib figure and axes for plotting random walks.

    Parameters:
    - ndim (int): The number of dimensions for the walkers.

    Returns:
    - Tuple[plt.Figure, Union[plt.Axes, p3.axes3d.Axes3D]]: The created figure and axes to plot on.
    """
    # Instantiate plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d') if ndim == 3 else fig.add_subplot(111)

    # Set title and labels
    ax.set_title(f'Random Walk - {ndim}D')
    if ndim == 1:
        ax.set_xlabel('Step')
        ax.set_ylabel('x')
    elif ndim == 2:
        ax.set_xlabel('x')
        ax.set_ylabel('y')
    elif ndim == 3:
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')

    return fig, ax


def update(frame: int, ax: Union[plt.Axes, p3.axes3d.Axes3D], rwalkers: List[RandomWalker], stable_lims: bool) -> List[Union[matplotlib.lines.Line2D, mpl_toolkits.mplot3d.art3d.Line3D]]:
    """
    Update function for the animation. Called by matplotlib's FuncAnimation to update the plot for each frame of the
    animation.

    Parameters:
    - frame (int):                            The current animation frame number.
    - ax (Union[plt.Axes, p3.axes3d.Axes3D]): The axes on which to plot.
    - rwalkers (List[RandomWalker]):          List of RandomWalker instances to visualize.
    - stable_lims (bool):                     Whether to keep the axes limits constant when animating or not.

    Returns:
    - List[Union[matplotlib.lines.Line2D, mpl_toolkits.mplot3d.art3d.Line3D]]: List of artists representing the plotted
                                                                               elements.
    """
    artists = []

    for rwalker in rwalkers:
        rwalker.plot_track(ax, frame, stable_lims)
        artists.extend(ax.lines)

    return artists


def run_animation(rwalkers: List[RandomWalker], ndim: int, nsteps: int, stable_lims: bool, save: bool, name: str) -> None:
    """
    Run the animation of random walker simulations.

    Parameters:
    - rwalkers (List[RandomWalker]): List of RandomWalker instances to visualize.
    - ndim (int):                    The number of dimensions for the walkers.
    - nsteps (int):                  The number of steps in each random walk.
    - stable_lims (bool):            Whether to keep the axes limits constant when animating or not.
    - save (bool):                   Whether to save the resulting figure to a file.
    - name (string):                 Name of the file to save
    """
    fig, ax = setup_axes(ndim)

    # Run the animation
    animation = FuncAnimation(
        fig,
        update,
        fargs=(ax, rwalkers, stable_lims),
        frames=nsteps,
        interval=min(1 / (nsteps * 2), 0.5),
        repeat=False
    )

    if save:
        path = f"src/images/plots{ndim}d"
        os.makedirs(path, exist_ok=True)
        #animation.save(os.path.join(path, f"{name}.gif"), writer='pillow', fps=30)
        fig.savefig(os.path.join(path, f"{name}.png"), dpi=200)

    plt.show()


def run_plot(rwalkers: List[RandomWalker], ndim: int, save: bool, name: str) -> None:
    """
    Create a static plot of the random walks.

    Parameters:
    - rwalkers (List[RandomWalker]): List of RandomWalker instances to visualize.
    - ndim (int):                    The number of dimensions for the walkers.
    - save (bool):                   Whether to save the resulting figure to a file.
    - name (string):                 Name of the file to save
    """
    fig, ax = setup_axes(ndim)

    for rwalker in rwalkers:
        rwalker.plot_track(ax)

    if save:
        path = f"src/images/plots{ndim}d"
        os.makedirs(path, exist_ok=True)
        fig.savefig(os.path.join(path, f"{name}.png"), dpi=200)

    plt.show()
