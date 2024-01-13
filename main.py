import numpy as np
import matplotlib
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import tkinter as tk
from tkinter import ttk
from typing import List, Tuple
from random_walker import RandomWalker

matplotlib.use("TkAgg")


def update(frame: int, ax: plt.Axes, rwalkers: List[RandomWalker], stable_lims: bool) -> List[plt.Line2D]:
    artists = []
    ax.clear()

    for rwalker in rwalkers:
        rwalker.plot_track(ax, frame, stable_lims)
        artists.extend(ax.lines)

    return artists


def run_simulations(start: Tuple[float, ...], ndim: int, seed: List[int], nwalkers: int, nsteps: int) \
                                                                                                -> List[RandomWalker]:
    rwalkers = []
    for i in range(nwalkers):
        rwalker = RandomWalker(start=start, ndim=ndim, seed=seed[i])
        rwalker.random_walk(nsteps)
        rwalkers.append(rwalker)

    return rwalkers


def run_animation(rwalkers: List[RandomWalker], ndim: int, nsteps: int, stable_lims: bool) -> None:
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d') if ndim == 3 else fig.add_subplot(111)

    animation = FuncAnimation(
        fig,
        update,
        fargs=(ax, rwalkers, stable_lims,),
        frames=nsteps,
        interval=min(1 / nsteps, 0.5),
        repeat=False
    )

    plt.show()


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Walker Simulation")

        self.reproducible = tk.BooleanVar(value=True)
        self.stable_lims = tk.BooleanVar(value=True)
        self.ndim = tk.IntVar(value=1)
        self.start = tk.StringVar(value="(0,)")
        self.nsteps = tk.IntVar(value=100)
        self.nwalkers = tk.IntVar(value=20)

        self.seed_start = tk.IntVar(value=1)

        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self.root, text="Reproducible:").grid(row=0, column=0, sticky="w")
        ttk.Checkbutton(self.root, variable=self.reproducible).grid(row=0, column=1, sticky="w")

        ttk.Label(self.root, text="Stable Limits:").grid(row=1, column=0, sticky="w")
        ttk.Checkbutton(self.root, variable=self.stable_lims).grid(row=1, column=1, sticky="w")

        ttk.Label(self.root, text="Number of Dimensions:").grid(row=2, column=0, sticky="w")
        ttk.Entry(self.root, textvariable=self.ndim).grid(row=2, column=1, sticky="w")

        ttk.Label(self.root, text="Start Position:").grid(row=3, column=0, sticky="w")
        ttk.Entry(self.root, textvariable=self.start).grid(row=3, column=1, sticky="w")

        ttk.Label(self.root, text="Number of Steps:").grid(row=4, column=0, sticky="w")
        ttk.Entry(self.root, textvariable=self.nsteps).grid(row=4, column=1, sticky="w")

        ttk.Label(self.root, text="Number of Walkers:").grid(row=5, column=0, sticky="w")
        ttk.Entry(self.root, textvariable=self.nwalkers).grid(row=5, column=1, sticky="w")

        ttk.Button(self.root, text="Run Simulations", command=self.run_simulations).grid(row=6, column=0, columnspan=2)

    def run_simulations(self):
        np.random.seed()
        seeds = [i + 1 for i in range(self.nsteps.get())] if self.reproducible else [-1] * self.nsteps.get()
        rwalkers = run_simulations(eval(self.start.get()), self.ndim.get(), seeds, self.nwalkers.get(), self.nsteps.get())
        run_animation(rwalkers, self.ndim.get(), self.nsteps.get(), self.stable_lims.get())


def main():
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
