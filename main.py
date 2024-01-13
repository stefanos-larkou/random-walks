import matplotlib
from matplotlib.animation import FuncAnimation
from matplotlib import pyplot as plt
from random_walker import RandomWalker

matplotlib.use("TkAgg")

REPRODUCIBLE = True
STABLE_LIMS = True
NDIM = 1
START = (0,) * NDIM
NSTEPS = 100
SEED = [i + 1 for i in range(NSTEPS)] if REPRODUCIBLE else [-1] * NSTEPS
NWALKERS = 20


def update(frame, ax, rwalkers):
    artists = []
    ax.clear()

    for rwalker in rwalkers:
        rwalker.plot_track(ax, frame, STABLE_LIMS)
        artists.extend(ax.lines)

    return artists


if __name__ == "__main__":
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d') if NDIM == 3 else fig.add_subplot(111)

    rwalkers = []
    for i in range(NWALKERS):
        rwalker = RandomWalker(start=START, ndim=NDIM, seed=SEED[i])
        rwalker.random_walk(NSTEPS)
        rwalkers.append(rwalker)

    ani = FuncAnimation(fig, update, fargs=(ax, rwalkers,), frames=NSTEPS, interval=min(1 / NSTEPS, 0.5), repeat=False)
    plt.show()
