import matplotlib
from matplotlib.animation import FuncAnimation
from matplotlib import pyplot as plt
from src.random_walker import RandomWalker
from typing import List, Tuple

matplotlib.use("TkAgg")

# Configuration variables
REPRODUCIBLE = True
STABLE_LIMS = True
NDIM = 3
START = (0,) * NDIM
NSTEPS = 100
SEED = [i + 1 for i in range(NSTEPS)] if REPRODUCIBLE else [-1] * NSTEPS
NWALKERS = 20


def update(frame: int, ax: plt.Axes, rwalkers: List[RandomWalker], stable_lims: bool) -> List[plt.Line2D]:
    """
    Update function for the animation of random walk simulations. This function is called by Matplotlib's FuncAnimation
    to update the plot for each frame of the animation.

    Parameters:
    - frame (int):                     The current animation frame number.
    - ax (matplotlib.axes._axes.Axes): The axes on which to plot.
    - rwalkers (List[RandomWalker]):   List of RandomWalker instances to visualize.

    Returns:
    List[matplotlib.lines.Line2D]: List of artists representing the plotted elements.
    """
    artists = []
    ax.clear()

    for rwalker in rwalkers:
        rwalker.plot_track(ax, frame, stable_lims)
        artists.extend(ax.lines)

    return artists


def run_examples_animation(start: Tuple[float, ...], ndim: int, seed: List[int], nwalkers: int, nsteps: int, stable_lims: bool) -> None:
    """
    Run an animation of random walk simulations and plot the results.

    This function demonstrates the usage of the RandomWalker class by creating instances with the specified starting
    position, number of dimensions, and seeds.
    It generates random walks for multiple walkers, plots the tracks, and displays the animation using Matplotlib.

    Each frame in the animation corresponds to a step in the random walk. The animation shows the paths of multiple
    random walkers simultaneously.

    Parameters:
    - start (Tuple[float, ...]): The starting position of the walkers.
    - ndim (int):                The number of dimensions for the walkers.
    - seed (List[int]):          List of random seeds for reproducibility.
    - nwalkers (int):            The number of random walkers to simulate.
    - nsteps (int):              The number of steps in each random walk.
    - stable_lims (bool):        Whether to keep the axes limits constant when animating.
    """
    # Instantiate plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d') if ndim == 3 else fig.add_subplot(111)

    # Instantiate random walkers and perform random walks
    rwalkers = []
    for i in range(nwalkers):
        rwalker = RandomWalker(start=start, ndim=ndim, seed=seed[i])
        rwalker.random_walk(nsteps)
        rwalkers.append(rwalker)

    # Plot the animation
    animation = FuncAnimation(
        fig,
        update,
        fargs=(ax, rwalkers, stable_lims,),
        frames=nsteps,
        interval=min(1 / nsteps, 0.5),
        repeat=False
    )

    plt.show()


if __name__ == "__main__":
    run_examples_animation(START, NDIM, SEED, NWALKERS, NSTEPS, STABLE_LIMS)
