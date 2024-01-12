import matplotlib.pyplot as plt
from random_walker import RandomWalker

if __name__ == "__main__":
    # Example Usage
    fig = plt.figure()
    ax = fig.add_subplot(111)
    for i in range(20):
        rwalker = RandomWalker(start=(0,), ndim=1)
        rwalker.random_walk(1000)
        rwalker.plot_track(ax)

    plt.show()

    fig = plt.figure()
    ax = fig.add_subplot(111)
    for i in range(20):
        rwalker = RandomWalker(start=(0, 0), ndim=2)
        rwalker.random_walk(1000)
        rwalker.plot_track(ax)

    plt.show()

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for i in range(20):
        rwalker = RandomWalker(start=(0, 0, 0), ndim=3)
        rwalker.random_walk(1000)
        rwalker.plot_track(ax)

    plt.show()
