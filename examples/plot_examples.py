from typing import List
import matplotlib.pyplot as plt
from src.random_walker import RandomWalker

# Configuration variables
REPRODUCIBLE = True
NSTEPS = 100
SEED = [i + 1 for i in range(NSTEPS)] if REPRODUCIBLE else [-1] * NSTEPS
NWALKERS = 20


def run_examples(seed: List[int], nwalkers: int, nsteps: int) -> None:
    """
    Run random walk simulations and plot the results.

    This function demonstrates the usage of the RandomWalker class by creating instances with the specified and seeds
    starting at the origin.
    It generates random walks for multiple walkers, plots the tracks, and displays the animation using matplotlib.

    Examples:
    - One-dimensional random walk.
    - Two-dimensional random walk.
    - Three-dimensional random walk.

    Each instance performs a random walk of `nsteps` steps, and the resulting tracks are plotted on separate subplots.

    Parameters:
    - seed (List[int]): List of random seeds for reproducibility.
    - nwalkers (int):                The number of random walkers to simulate.
    - nsteps (int):                  The number of steps in each random walk.
    """
    # One-dimensional random walk
    fig = plt.figure()
    ax = fig.add_subplot(111)
    for i in range(nwalkers):
        rwalker = RandomWalker(start=(0,), ndim=1, seed=seed[i])
        rwalker.random_walk(nsteps)
        rwalker.plot_track(ax)

    plt.show()

    # Two-dimensional random walk
    fig = plt.figure()
    ax = fig.add_subplot(111)
    for i in range(nwalkers):
        rwalker = RandomWalker(start=(0, 0), ndim=2, seed=seed[i])
        rwalker.random_walk(nsteps)
        rwalker.plot_track(ax)

    plt.show()

    # Three-dimensional random walk
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for i in range(nwalkers):
        rwalker = RandomWalker(start=(0, 0, 0), ndim=3, seed=seed[i])
        rwalker.random_walk(nsteps)
        rwalker.plot_track(ax)

    plt.show()


if __name__ == "__main__":
    run_examples(SEED, NWALKERS, NSTEPS)
