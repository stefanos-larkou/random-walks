import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox
import TKinterModernThemes as TKMT
from typing import List, Tuple
import re
from random_walker import RandomWalker
from visualisation import run_animation, run_plot


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
    - animate (tk.BooleanVar):      Whether to create an animation or simply plot the random walks.
    - save (tk.BooleanVar):         Whether to save the resulting figure to a file.
    - mame (tk.StringVar):          Name of the file to be saved. Must start and end with alphanumeric characters and
                                    only whitespaces, hyphens, and underscores are allowed.

    - seed_label (ttk.Label):       Seed input label stored to toggle visibility.
    - seed_entry (ttk.Entry):       Seed input stored to toggle visibility.
    - name_label (ttk.Label):       Name input label stored to toggle visibility.
    - name_entry (ttk.Entry):       Name input stored to toggle visibility.

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
        self.animate = tk.BooleanVar(value=True)
        self.save = tk.BooleanVar(value=False)
        self.name = tk.StringVar(value="result")

        self.seed_label = None
        self.seed_entry = None
        self.name_label = None
        self.name_entry = None

        self.create_widgets()

    def create_widgets(self) -> None:
        """
        Create GUI widgets for the random walk parameter input.
        """
        ttk.Style().configure("TLabel", padding=(0, 8))
        ttk.Style().configure("TButton", padding=(10, 10))

        ttk.Label(self.root, text="Reproducible:").grid(row=0, column=0, sticky="w")
        ttk.Checkbutton(self.root, variable=self.reproducible, command=self.toggle_seed_entry).grid(row=0, column=1)

        self.seed_label = ttk.Label(self.root, text="Seed start:")
        self.seed_label.grid(row=1, column=0, sticky="w")
        self.seed_entry = ttk.Entry(self.root, textvariable=self.seed_start)
        self.seed_entry.grid(row=1, column=1)

        ttk.Label(self.root, text="Stable limits:").grid(row=2, column=0, sticky="w")
        ttk.Checkbutton(self.root, variable=self.stable_lims).grid(row=2, column=1)

        ttk.Label(self.root, text="Number of dimensions:").grid(row=3, column=0, sticky="w")
        ttk.Entry(self.root, textvariable=self.ndim).grid(row=3, column=1)

        ttk.Label(self.root, text="Start position:").grid(row=4, column=0, sticky="w")
        ttk.Entry(self.root, textvariable=self.start).grid(row=4, column=1)

        ttk.Label(self.root, text="Number of steps:").grid(row=5, column=0, sticky="w")
        ttk.Entry(self.root, textvariable=self.nsteps).grid(row=5, column=1)

        ttk.Label(self.root, text="Number of walkers:").grid(row=6, column=0, sticky="w")
        ttk.Entry(self.root, textvariable=self.nwalkers).grid(row=6, column=1)

        ttk.Label(self.root, text="Animate:").grid(row=7, column=0, sticky="w")
        ttk.Checkbutton(self.root, variable=self.animate).grid(row=7, column=1)

        ttk.Label(self.root, text="Save result:").grid(row=8, column=0, sticky="w")
        ttk.Checkbutton(self.root, variable=self.save, command=self.toggle_name_entry).grid(row=8, column=1)

        self.name_label = ttk.Label(self.root, text="Filename:")
        self.name_label.grid(row=9, column=0, sticky="w")
        self.name_entry = ttk.Entry(self.root, textvariable=self.name)
        self.name_entry.grid(row=9, column=1)

        ttk.Button(self.root, text="Run Simulations", command=self.run_simulations).grid(row=10, column=0, columnspan=2)

        self.name_entry.grid_remove()
        self.name_label.grid_remove()

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

    def toggle_name_entry(self) -> None:
        """
        Toggle visibility of seed input based on the reproducibility checkbox.
        """
        if self.save.get():
            self.name_entry.grid()
            self.name_label.grid()
        else:
            self.name_entry.grid_remove()
            self.name_label.grid_remove()

    def run_simulations(self) -> None:
        """
        Perform some input validation and run random walker simulations based on user input.
        """
        try:
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
            if not self._validate_filename(self.name.get()):
                messagebox.showerror("Error", "Filename must begin and end with alphanumeric characters. "
                                                            "Only whitespaces, hyphens, and underscores are allowed "
                                                            "between.")
                return

            np.random.seed()
            seeds = [i + self.seed_start.get() for i in range(self.nsteps.get())] if self.reproducible.get() else [-1] * self.nsteps.get()
            rwalkers = run_simulations(eval(self.start.get()), self.ndim.get(), seeds, self.nwalkers.get(), self.nsteps.get())

            if self.animate.get():
                run_animation(rwalkers, self.ndim.get(), self.nsteps.get(), self.stable_lims.get(), self.save.get(), self.name.get())
            else:
                run_plot(rwalkers, self.ndim.get(), self.save.get(), self.name.get())
        except tk.TclError:
            messagebox.showerror("Error", "Please enter valid inputs.")

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

    def _validate_filename(self, name):
        regex = re.compile(r"^[a-zA-Z0-9]([a-zA-Z0-9_ -]*[a-zA-Z0-9])?$")
        return regex.match(name)


def main():
    window = TKMT.ThemedTKinterFrame("Random Walk Simulation", "azure", "light")
    icon_path = "images\\icon.ico"
    window_icon = tk.PhotoImage(file=icon_path)
    window.root.tk.call("wm", "iconphoto", window.root._w, window_icon)
    window.root.resizable(False, False)
    App(window.root)
    window.root.mainloop()


if __name__ == "__main__":
    main()
