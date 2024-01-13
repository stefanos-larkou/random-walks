import matplotlib.pyplot as plt
from random_walker import RandomWalker


def run_examples() -> None:
    """
    Run random walk simulations and plot the results.

    This function demonstrates the usage of the RandomWalker class by creating instances
    with different starting positions and numbers of dimensions. It generates random walks,
    plots the tracks, and displays the plots using Matplotlib.

    Examples:
    - One-dimensional random walk with 20 instances starting at position (0).
    - Two-dimensional random walk with 20 instances starting at position (0, 0).
    - Three-dimensional random walk with 20 instances starting at position (0, 0, 0).

    Each instance performs a random walk of 100 steps, and the resulting tracks are
    plotted on separate subplots.
    """
    # Example Usage
    fig = plt.figure()
    ax = fig.add_subplot(111)
    for i in range(20):
        rwalker = RandomWalker(start=(0,), ndim=1)
        rwalker.random_walk(100)
        rwalker.plot_track(ax)

    plt.show()

    fig = plt.figure()
    ax = fig.add_subplot(111)
    for i in range(20):
        rwalker = RandomWalker(start=(0, 0), ndim=2)
        rwalker.random_walk(100)
        rwalker.plot_track(ax)

    plt.show()

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for i in range(20):
        rwalker = RandomWalker(start=(0, 0, 0), ndim=3)
        rwalker.random_walk(100)
        rwalker.plot_track(ax)

    plt.show()


if __name__ == "__main__":
    run_examples()
