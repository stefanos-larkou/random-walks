import numpy as np
import matplotlib
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import tkinter as tk
from tkinter import ttk, messagebox
import TKinterModernThemes as TKMT
from typing import List, Tuple
from random_walker import RandomWalker

matplotlib.use("TkAgg")


def update(frame: int, ax: plt.Axes, rwalkers: List[RandomWalker], stable_lims: bool) -> List[plt.Line2D]:
    """
    Update function for the animation. Called by matplotlib's FuncAnimation to update the plot for each frame of the
    animation.

    Parameters:
    - frame (int):                   The current animation frame number.
    - ax (plt.Axes):                 The axes on which to plot.
    - rwalkers (List[RandomWalker]): List of RandomWalker instances to visualize.
    - stable_lims (bool):            Whether to keep the axes limits constant when animating or not.

    Returns:
    - List[plt.Line2D]: List of artists representing the plotted elements.
    """
    artists = []

    for rwalker in rwalkers:
        rwalker.plot_track(ax, frame, stable_lims)
        artists.extend(ax.lines)

    return artists


def run_simulations(start: Tuple[float, ...], ndim: int, seed: List[int], nwalkers: int, nsteps: int) -> List[RandomWalker]:
    """
    Run random walker simulations.

    Parameters:
    - start (Tuple[float, ...]): The starting position of the walkers.
    - ndim (int):                The number of dimensions for the walkers.
    - seed (List[int]):          List of random seeds for reproducibility.
    - nwalkers (int):            The number of random walks to simulate.
    - nsteps (int):              The number of steps in each random walk.

    Returns:
    - List[RandomWalker]: List of RandomWalker objects.
    """
    rwalkers = []
    for i in range(nwalkers):
        rwalker = RandomWalker(start=start, ndim=ndim, seed=seed[i])
        rwalker.random_walk(nsteps)
        rwalkers.append(rwalker)

    return rwalkers


def run_animation(rwalkers: List[RandomWalker], ndim: int, nsteps: int, stable_lims: bool) -> None:
    """
    Run the animation of random walker simulations.

    Parameters:
    - rwalkers (List[RandomWalker]): List of RandomWalker instances to visualize.
    - ndim (int):                    The number of dimensions for the walkers.
    - nsteps (int):                  The number of steps in each random walk.
    - stable_lims (bool):            Whether to keep the axes limits constant when animating or not.
    """
    # Create plot
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

    # Run the animation
    animation = FuncAnimation(
        fig,
        update,
        fargs=(ax, rwalkers, stable_lims),
        frames=nsteps,
        interval=min(1 / (nsteps * 2), 0.5),
        repeat=False
    )

    plt.show()


class App:
    """
    GUI application for the random walk simulation.

    Attributes:
    - root (tk.Tk):                 Tkinter root window.
    - reproducible (tk.BooleanVar): Whether to set seeds to the random walks for a reproducible result.
    - stable_lims (tk.BooleanVar):  Whether to keep axes limits constant or not.
    - ndim (tk.IntVar):             Dimensions of the random walk.
    - start (tk.StringVar):         Common starting position of the random walks.
    - seed_start (tk.IntVar):       If reproducible is true, the seeds set to the random walks start from this value and
                                    increment by 1 for each random walk.
    - nsteps (tk.IntVar):           The number of steps of the random walks.
    - nwalkers (tk.IntVar):         The number of RandomWalker instances to create.

    - seed_label (ttk.Label):       Seed input label stored to toggle visibility.
    - seed_entry (ttk.Entry):       Seed input stored to toggle visibility.

    Methods:
    - create_widgets() -> None: Create GUI widgets for the random walk parameter input.
    - toggle_seed_entry() -> None: Toggle visibility of seed input based on the reproducibility checkbox.
    - run_simulations() -> None: Perform some input validation and run random walker simulations based on user input.
    """
    def __init__(self, root: tk.Tk) -> None:
        """
        Initialize the GUI application for the random walk simulation.

        Parameters:
        - root (tk.Tk): Tkinter root window.
        """
        self.root = root
        self.root.title("Random Walker Simulation")

        self.reproducible = tk.BooleanVar(value=True)
        self.stable_lims = tk.BooleanVar(value=True)
        self.ndim = tk.IntVar(value=1)
        self.start = tk.StringVar(value="(0,)")
        self.seed_start = tk.IntVar(value=1)
        self.seed_start = tk.IntVar(value=1)
        self.nsteps = tk.IntVar(value=100)
        self.nwalkers = tk.IntVar(value=20)

        self.seed_label = None
        self.seed_entry = None

        self.create_widgets()

    def create_widgets(self) -> None:
        """
        Create GUI widgets for the random walk parameter input.
        """
        ttk.Style().configure("TLabel", padding=(0, 8))
        ttk.Style().configure("TButton", padding=(10, 10))

        ttk.Label(self.root, text="Reproducible:").grid(row=0, column=0, sticky="w")
        ttk.Checkbutton(self.root, variable=self.reproducible, command=self.toggle_seed_entry).grid(row=0, column=1)

        self.seed_label = ttk.Label(self.root, text="Seed Start:")
        self.seed_label.grid(row=1, column=0, sticky="w")
        self.seed_entry = ttk.Entry(self.root, textvariable=self.seed_start)
        self.seed_entry.grid(row=1, column=1)

        ttk.Label(self.root, text="Stable Limits:").grid(row=2, column=0, sticky="w")
        ttk.Checkbutton(self.root, variable=self.stable_lims).grid(row=2, column=1)

        ttk.Label(self.root, text="Number of Dimensions:").grid(row=3, column=0, sticky="w")
        ttk.Entry(self.root, textvariable=self.ndim).grid(row=3, column=1)

        ttk.Label(self.root, text="Start Position:").grid(row=4, column=0, sticky="w")
        ttk.Entry(self.root, textvariable=self.start).grid(row=4, column=1)

        ttk.Label(self.root, text="Number of Steps:").grid(row=5, column=0, sticky="w")
        ttk.Entry(self.root, textvariable=self.nsteps).grid(row=5, column=1)

        ttk.Label(self.root, text="Number of Walkers:").grid(row=6, column=0, sticky="w")
        ttk.Entry(self.root, textvariable=self.nwalkers).grid(row=6, column=1)

        ttk.Button(self.root, text="Run Simulations", command=self.run_simulations).grid(row=7, column=0, columnspan=2)

    def toggle_seed_entry(self) -> None:
        """
        Toggle visibility of seed input based on the reproducibility checkbox.
        """
        if self.reproducible.get():
            self.seed_entry.grid()
            self.seed_label.grid()
        else:
            self.seed_entry.grid_remove()
            self.seed_label.grid_remove()

    def run_simulations(self) -> None:
        """
        Perform some input validation and run random walker simulations based on user input.
        """
        if not self._validate_dimensions(self.ndim.get()):
            messagebox.showerror("Error", "Number of dimensions must be an integer between 1 and 3.")
            return
        if not self._validate_start(self.start.get()):
            messagebox.showerror("Error", "Invalid start position format or length.")
            return
        if not self._validate_positive_int(self.seed_start.get()):
            messagebox.showerror("Error", "Starting seed value must be a positive integer.")
            return
        if not self._validate_positive_int(self.nsteps.get()):
            messagebox.showerror("Error", "Number of steps must be a positive integer.")
            return
        if not self._validate_positive_int(self.nwalkers.get()):
            messagebox.showerror("Error", "Number of walkers must be a positive integer.")
            return

        np.random.seed()
        seeds = [i + self.seed_start.get() for i in range(self.nsteps.get())] if self.reproducible.get() else [-1] * self.nsteps.get()
        rwalkers = run_simulations(eval(self.start.get()), self.ndim.get(), seeds, self.nwalkers.get(), self.nsteps.get())
        run_animation(rwalkers, self.ndim.get(), self.nsteps.get(), self.stable_lims.get())

    def _validate_dimensions(self, ndim: int) -> bool:
        """
        Ensure the number of dimensions is between 1 and 3 inclusive.

        Parameters:
        - ndim (int): Number of dimensions.

        Returns:
        - bool: True if the number of dimensions is valid, False otherwise.
        """
        try:
            ndim = int(ndim)
            return 1 <= ndim <= 3
        except ValueError:
            return False

    def _validate_start(self, start: str) -> bool:
        """
        Ensure the start position is a tuple of integers or floats of length equal to the number of dimensions.

        Parameters:
        - start (str): Start position.

        Returns:
        - bool: True if the start position is valid, False otherwise.
        """
        try:
            start = eval(start)
            return isinstance(start, tuple) and all(isinstance(val, (int, float)) for val in start) and len(start) == self.ndim.get()
        except ValueError:
            return False

    def _validate_positive_int(self, value: int) -> bool:
        """
        Ensure an input is a positive integer number.

        Parameters:
        - value (int): Value to validate.

        Returns:
        - bool: True if the value is valid, False otherwise.
        """
        try:
            value = int(value)
            return value > 0
        except ValueError:
            return False


def main():
    window = TKMT.ThemedTKinterFrame("Random Walk Simulation", "azure", "light")
    icon_path = 'src\\images\\icon.ico'
    window_icon = tk.PhotoImage(file=icon_path)
    window.root.tk.call('wm', 'iconphoto', window.root._w, window_icon)
    window.root.resizable(False, False)
    App(window.root)
    window.root.mainloop()


if __name__ == "__main__":
    main()
