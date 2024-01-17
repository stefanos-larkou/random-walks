import os
import sys
import re
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.style as mplstyle
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk, messagebox
import TKinterModernThemes as TKMT
from typing import List, Tuple
from random_walker import RandomWalker
from visualisation import run_animation, run_plot, plot_distance_hist, plot_distance_meshgrid


def run_simulations(start: Tuple[float, ...], ndim: int, allow_diagonals: bool, seed: List[int], nwalkers: int, nsteps: int) -> List[RandomWalker]:
    """
    Run random walker simulations.

    Parameters:
    - start (Tuple[float, ...]): The starting position of the walkers.
    - ndim (int):                The number of dimensions for the walkers.
    - allow_diagonals (bool):    Whether to allow diagonal movements.
    - seed (List[int]):          List of random seeds for reproducibility.
    - nwalkers (int):            The number of random walks to simulate.
    - nsteps (int):              The number of steps in each random walk.

    Returns:
    - List[RandomWalker]: List of RandomWalker objects.
    """
    # Create walker objects and run the random walks
    rwalkers = []
    for i in range(nwalkers):
        rwalker = RandomWalker(start=start, ndim=ndim, allow_diagonals=allow_diagonals, seed=seed[i])
        rwalker.random_walk(nsteps)
        rwalkers.append(rwalker)

    return rwalkers


class App:
    """
    GUI application for the random walk simulation.

    Attributes:
    - root (tk.Tk):                    Tkinter root window.
    - reproducible (tk.BooleanVar):    Whether to set seeds to the random walks for a reproducible result.
    - stable_lims (tk.BooleanVar):     Whether to keep axes limits constant or not.
    - allow_diagonals (tk.BooleanVar): Whether to allow diagonal movements.
    - ndim (tk.IntVar):                Dimensions of the random walk.
    - start (tk.StringVar):            Common starting position of the random walks.
    - seed_start (tk.IntVar):          If reproducible is true, the seeds set to the random walks start from this value
                                       and increment by 1 for each random walk.
    - nsteps (tk.IntVar):              The number of steps of the random walks.
    - nwalkers (tk.IntVar):            The number of RandomWalker instances to create.
    - animate (tk.BooleanVar):         Whether to create an animation or simply plot the random walks.
    - style (tk.StringVar):            Style to use when plotting.
    - save (tk.BooleanVar):            Whether to save the resulting figure to a file.
    - mame (tk.StringVar):             Name of the file to be saved. Must start and end with alphanumeric characters and
                                       only whitespaces, hyphens, and underscores are allowed.

    - seed_label (ttk.Label):          Seed input label stored to toggle visibility.
    - stable_lims_label (ttk.Label):   Stable limits input label stored to toggle visibility.
    - name_label (ttk.Label):          Name input label stored to toggle visibility.

    - seed_entry (ttk.Entry):          Seed input stored to toggle visibility.
    - name_entry (ttk.Entry):          Name input stored to toggle visibility.
    - ndim_entry (ttk.Entry):          Dimensionality input stored to bind to validation function.
    - start_entry (ttk.Entry):         Starting position input stored to bind to validation function.
    - nsteps_entry (ttk.Entry):        Number of steps input stored to bind to validation function.
    - nwalkers_entry (ttk.Entry):      Number of random walks input stored to bind to validation function.
    - style_combobox (ttk.Combobox):   Style input stored to bind to validation function.
    - stable_lims_checkbutton (ttk.Checkbutton):
                                       Stable limits input stored to toggle visibility.
    - name_entry (ttk.Entry):          Filename input stored to bind to validation function.

    - styles (List[str]):              List of matplotlib styles
    - animation (matplotlib.animation.FuncAnimation):
                                       The animation to be plotted.
    - fig (matplotlib.figure.Figure):
                                       The figure on which the plot will appear.
    - canvas (matplotlib.backends.backend_tkagg.FigureCanvasTkAgg):
                                       Canvas to be added to the grid containing the plotted figure.
    - mesh_fig (matplotlib.figure.Figure):
                                       The figure on which the meshgrid will appear.
    - mesh_canvas (matplotlib.backends.backend_tkagg.FigureCanvasTkAgg):
                                       Canvas to be added to the grid containing the meshgrid of distances of the random
                                       walk simulation.
    - hist_fig (matplotlib.figure.Figure):
                                       The figure on which the histogram will appear.
    - hist_canvas (matplotlib.backends.backend_tkagg.FigureCanvasTkAgg):
                                       Canvas to be added to the grid containing the histogram of final distances of the
                                       random walk simulation.

    Methods:
    - create_widgets() -> None:    Create GUI widgets for the random walk parameter input.
    - set_min_win_size() -> None:  Set the minimum size of the window.
    - change_start_dim() -> None:  Change default value of the starting positions based on the number of dimensions.
    - toggle_seed_entry() -> None: Toggle visibility of seed input based on the reproducibility checkbox.
    - toggle_stable_lims_checkbutton() -> None:
                                   Toggle visibility of the stable axes limits checkbox.
    - toggle_name_entry() -> None: Toggle visibility of filename input based on the save result checkbox.
    - run_simulations() -> None:   Perform some input validation and run random walker simulations based on user input.
    """
    def __init__(self, root: tk.Tk) -> None:
        """
        Initialize the GUI application for the random walk simulation.

        Parameters:
        - root (tk.Tk): Tkinter root window.
        """
        # Set root
        self.root = root
        self.root.title("Random Walker Simulation")

        # Initialise input values
        self.reproducible = tk.BooleanVar(value=True)
        self.stable_lims = tk.BooleanVar(value=True)
        self.allow_diagonals = tk.BooleanVar(value=False)
        self.ndim = tk.IntVar(value=1)
        self.start = tk.StringVar(value="(0,)")
        self.seed_start = tk.IntVar(value=1)
        self.nsteps = tk.IntVar(value=100)
        self.nwalkers = tk.IntVar(value=20)
        self.animate = tk.BooleanVar(value=True)
        self.style = tk.StringVar(value="default")
        self.save = tk.BooleanVar(value=False)
        self.name = tk.StringVar(value="result")

        # Initialise input objects that need to be stored
        self.seed_label = None
        self.stable_lims_label = None
        self.name_label = None
        self.ndim_entry = None
        self.start_entry = None
        self.seed_entry = None
        self.nsteps_entry = None
        self.nwalkers_entry = None
        self.style_combobox = None
        self.stable_lims_checkbutton = None
        self.name_entry = None

        # Plotting related attributes
        self.styles = [style for style in mplstyle.available if not style.startswith("_")]
        self.styles.sort(key=lambda x: str(x).lower())
        self.styles.insert(0, "default")

        self.animation = None
        self.fig = None
        self.canvas = None
        self.mesh_fig = None
        self.mesh_canvas = None
        self.hist_fig = None
        self.hist_canvas = None

        # Set up widgets
        self.create_widgets()

    def create_widgets(self) -> None:
        """
        Create GUI widgets for the random walk parameter input. Non-checkbox inputs are validated when the user attempts
        to focus on something else.
        """
        # Set up widgets, add bindings to validation and toggling functions
        ttk.Label(self.root, text="Number of dimensions:").grid(row=0, column=0, sticky="w", padx=(10, 0))
        self.ndim_entry = ttk.Entry(self.root, textvariable=self.ndim)
        self.ndim_entry.grid(row=0, column=1, padx=(5, 10))
        self.ndim_entry.bind("<KeyRelease>", lambda event: self.change_start_dim())
        self.ndim_entry.bind("<FocusOut>", lambda event: self._validate_dimensions())

        ttk.Label(self.root, text="Start position:").grid(row=1, column=0, sticky="w", padx=(10, 0))
        self.start_entry = ttk.Entry(self.root, textvariable=self.start)
        self.start_entry.grid(row=1, column=1, padx=(5, 10))
        self.start_entry.bind("<FocusOut>", lambda event: self._validate_start())

        ttk.Label(self.root, text="Number of steps:").grid(row=2, column=0, sticky="w", padx=(10, 0))
        self.nsteps_entry = ttk.Entry(self.root, textvariable=self.nsteps)
        self.nsteps_entry.grid(row=2, column=1, padx=(5, 10))
        self.nsteps_entry.bind("<FocusOut>", lambda event: self._validate_positive_int(self.nsteps, "Number of steps ", self.nsteps_entry))

        ttk.Label(self.root, text="Number of walkers:").grid(row=3, column=0, sticky="w", padx=(10, 0))
        self.nwalkers_entry = ttk.Entry(self.root, textvariable=self.nwalkers)
        self.nwalkers_entry.grid(row=3, column=1, padx=(5, 10))
        self.nwalkers_entry.bind("<FocusOut>", lambda event: self._validate_positive_int(self.nwalkers, "Number of walkers ", self.nwalkers_entry))

        ttk.Label(self.root, text="Matplotlib Style:").grid(row=4, column=0, sticky="w", padx=(10, 0))
        self.style_combobox = ttk.Combobox(self.root, textvariable=self.style, values=self.styles)
        self.style_combobox.grid(row=4, column=1, padx=(5, 10))
        self.style_combobox.bind("<FocusOut>", lambda event: self._validate_style())

        ttk.Label(self.root, text="Diagonal movements:").grid(row=5, column=0, sticky="w", padx=(10, 0))
        ttk.Checkbutton(self.root, variable=self.allow_diagonals).grid(row=5, column=1, padx=(5, 10))

        ttk.Label(self.root, text="Reproducible:").grid(row=6, column=0, sticky="w", padx=(10, 0))
        ttk.Checkbutton(self.root, variable=self.reproducible, command=self.toggle_seed_entry).grid(row=6, column=1, padx=(5, 10))

        self.seed_label = ttk.Label(self.root, text="Seed start:")
        self.seed_label.grid(row=7, column=0, sticky="w", padx=(10, 0))
        self.seed_entry = ttk.Entry(self.root, textvariable=self.seed_start)
        self.seed_entry.grid(row=7, column=1, padx=(5, 10))
        self.seed_entry.bind("<FocusOut>", lambda event: self._validate_positive_int(self.seed_start, "Starting seed value ", self.seed_entry))

        ttk.Label(self.root, text="Animate:").grid(row=8, column=0, sticky="w", padx=(10, 0))
        ttk.Checkbutton(self.root, variable=self.animate, command=self.toggle_stable_lims_checkbutton).grid(row=8, column=1, padx=(5, 10))

        self.stable_lims_label = ttk.Label(self.root, text="Stable limits:")
        self.stable_lims_label.grid(row=9, column=0, sticky="w", padx=(10, 0))
        self.stable_lims_checkbutton = ttk.Checkbutton(self.root, variable=self.stable_lims)
        self.stable_lims_checkbutton.grid(row=9, column=1, padx=(5, 10))

        ttk.Label(self.root, text="Save result:").grid(row=10, column=0, sticky="w", padx=(10, 0))
        ttk.Checkbutton(self.root, variable=self.save, command=self.toggle_name_entry).grid(row=10, column=1, padx=(5, 10))

        self.name_label = ttk.Label(self.root, text="Filename:")
        self.name_label.grid(row=11, column=0, sticky="w", padx=(10, 0))
        self.name_entry = ttk.Entry(self.root, textvariable=self.name)
        self.name_entry.grid(row=11, column=1, padx=(5, 10))
        self.name_entry.bind("<FocusOut>", lambda event: self._validate_filename())

        ttk.Button(self.root, text="Run Simulations", command=self.run_simulations).grid(row=12, column=0, columnspan=2, pady=(10, 0))

        # Filename is hidden by default
        self.name_entry.grid_remove()
        self.name_label.grid_remove()

        # Generic widget configuration
        ttk.Style().configure("TLabel", padding=(0, 10))
        ttk.Style().configure("TButton", padding=(10, 10))

        # For dynamic resizing
        self.root.rowconfigure(13, minsize=10)
        for i in range(13):
            self.root.rowconfigure(i, weight=1)
        for i in range(2):
            self.root.columnconfigure(i, weight=1)

        # Set minimum window size after a short delay to ensure widgets are rendered
        self.root.after(100, self.set_min_win_size)
        self.root.after(100, lambda: self.root.maxsize(width=self.root.winfo_reqwidth(), height=self.root.winfo_reqheight()))

    def set_min_win_size(self) -> None:
        """
        Set the minimum size of the window.

        Determined by the minimum required width and height to keep all widgets visible.
        """
        self.root.minsize(width=self.root.winfo_reqwidth(), height=self.root.winfo_reqheight())

    def change_start_dim(self) -> None:
        """
        Change default value of the starting positions based on the number of dimensions.
        """
        try:
            ndim = int(self.ndim.get())
            if ndim == 1:
                self.start.set("(0,)")
            elif ndim == 2:
                self.start.set("(0, 0)")
            elif ndim == 3:
                self.start.set("(0, 0, 0)")
        except (ValueError, tk.TclError):
            pass

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
            self.seed_start.set(1)

    def toggle_stable_lims_checkbutton(self) -> None:
        """
        Toggle visibility of the stable axes limits checkbox.
        """
        if self.animate.get():
            self.stable_lims_checkbutton.grid()
            self.stable_lims_label.grid()
        else:
            self.stable_lims_checkbutton.grid_remove()
            self.stable_lims_label.grid_remove()
            self.stable_lims.set(True)

    def toggle_name_entry(self) -> None:
        """
        Toggle visibility of filename input based on the save result checkbox.
        """
        if self.save.get():
            self.name_entry.grid()
            self.name_label.grid()
        else:
            self.name_entry.grid_remove()
            self.name_label.grid_remove()
            self.name.set("result")

    def run_simulations(self) -> None:
        """
        Perform input validation again and run random walker simulations based on user input.
        """
        try:
            # Run validations again (not really needed)
            if not self._validate_dimensions(): return
            if not self._validate_start(): return
            if not self._validate_positive_int(self.seed_start, "Starting seed value ", self.seed_entry): return
            if not self._validate_positive_int(self.nsteps, "Number of steps ", self.nsteps_entry): return
            if not self._validate_positive_int(self.nwalkers, "Number of walkers ", self.nwalkers_entry): return
            if not self._validate_filename(): return
            self._validate_style()

            # Determine seed values and run random walk simulations
            np.random.seed()
            seeds = [i + self.seed_start.get() for i in range(self.nwalkers.get())] if self.reproducible.get() else [-1] * self.nwalkers.get()
            rwalkers = run_simulations(eval(self.start.get()), self.ndim.get(), self.allow_diagonals.get(), seeds, self.nwalkers.get(), self.nsteps.get())

            # Set Matplotlib style
            plt.style.use(self.style.get())

            # If something was already plotted, close it
            if self.fig is not None:
                self.animation = None
                plt.close(self.fig)
                self.canvas.get_tk_widget().grid_remove()

            if self.mesh_fig is not None:
                self.animation = None
                plt.close(self.mesh_fig)
                self.mesh_canvas.get_tk_widget().grid_remove()

            if self.hist_fig is not None:
                self.animation = None
                plt.close(self.hist_fig)
                self.hist_canvas.get_tk_widget().grid_remove()

            if self.animate.get():
                # Generate the animation
                self.animation, self.fig = run_animation(rwalkers, self.ndim.get(), self.nsteps.get(), self.stable_lims.get(), self.save.get(), self.name.get())
            else:
                # Generate the static plot
                self.fig = run_plot(rwalkers, self.ndim.get(), self.nsteps.get(), self.save.get(), self.name.get())

            # Place main figure
            rowspan = 7 if self.nwalkers.get() >= 5 else 13
            self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
            self.canvas.get_tk_widget().grid(row=0, column=2, rowspan=rowspan, padx=8, pady=8, columnspan=2)
            self.canvas.get_tk_widget()["borderwidth"] = 1
            self.canvas.get_tk_widget()["relief"] = "solid"

            if self.nwalkers.get() >= 5:
                # Place meshgrid
                self.mesh_fig = plot_distance_meshgrid(rwalkers)
                self.mesh_canvas = FigureCanvasTkAgg(self.mesh_fig, master=self.root)
                self.mesh_canvas.get_tk_widget().grid(row=7, column=2, rowspan=6, padx=8, pady=8)
                self.mesh_canvas.get_tk_widget()["borderwidth"] = 1
                self.mesh_canvas.get_tk_widget()["relief"] = "solid"

                # Place histogram
                self.hist_fig = plot_distance_hist(rwalkers)
                self.hist_canvas = FigureCanvasTkAgg(self.hist_fig, master=self.root)
                self.hist_canvas.get_tk_widget().grid(row=7, column=3, rowspan=6, padx=8, pady=8)
                self.hist_canvas.get_tk_widget()["borderwidth"] = 1
                self.hist_canvas.get_tk_widget()["relief"] = "solid"

            # Configure new columns
            self.root.columnconfigure(2, weight=1)
            if self.nwalkers.get() >= 5:
                self.root.columnconfigure(3, weight=1)

            # Set minimum window size after a short delay to ensure widgets are rendered
            self.root.maxsize(0, 0)
            self.root.after(100, self.set_min_win_size)
        except tk.TclError:
            # Just in case something went wrong
            messagebox.showerror("Error", "Please enter valid inputs.")

    def _validate_dimensions(self) -> bool:
        """
        Ensure the number of dimensions is an integer between 1 and 3 inclusive.

        Returns:
        - bool: True if the number of dimensions is valid, False otherwise.
        """
        try:
            if not (isinstance(self.ndim.get(), int) and 1 <= self.ndim.get() <= 3):
                messagebox.showerror("Error", "Number of dimensions must be an integer between 1 and 3.")
                self.ndim_entry.focus_set()
                return False
            self.ndim.set(int(self.ndim.get()))
            return True
        except (ValueError, tk.TclError):
            messagebox.showerror("Error", "Number of dimensions must be an integer between 1 and 3.")
            self.ndim_entry.focus_set()
            return False

    def _validate_start(self) -> bool:
        """
        Ensure the start position is a tuple of integers or floats of length equal to the number of dimensions.

        Returns:
        - bool: True if the start position is valid, False otherwise.
        """
        try:
            start = eval(self.start.get())
            if not isinstance(start, tuple) and all(isinstance(val, (int, float)) for val in start) and len(start) == self.ndim.get():
                messagebox.showerror("Error", "Invalid start position format or length.")
                self.start_entry.focus_set()
                return False
            return True
        except (ValueError, SyntaxError, TypeError, tk.TclError):
            messagebox.showerror("Error", "Invalid start position format or length.")
            self.start_entry.focus_set()
            return False

    @staticmethod
    def _validate_positive_int(value: tk.IntVar, text: str, entry: tk.Entry) -> bool:
        """
        Ensure an input is a positive integer number.

        Parameters:
        - value (tk.IntVar): Value to validate.
        - text (str):        Text to customise the error message.
        - entry (tk.Entry):  Input on which to focus if the validation fails.

        Returns:
        - bool: True if the value is valid, False otherwise.
        """
        try:
            if not (isinstance(value.get(), int) and value.get() > 0):
                messagebox.showerror("Error", f"{text} must be a positive integer.")
                entry.focus_set()
                return False
            value.set(int(value.get()))
            return True
        except (ValueError, tk.TclError):
            messagebox.showerror("Error", f"{text} must be a positive integer.")
            entry.focus_set()
            return False

    def _validate_style(self) -> None:
        """
        Ensure there is always a valid style in the combobox. If focused out of the combobox with an invalid style,
        reset to default.
        """
        if self.style.get() not in self.styles:
            self.style.set("default")

    def _validate_filename(self) -> bool:
        """
        Ensure the filename begins and ends with alphanumeric characters and only has whitespaces, hyphens or
        underscores in between.

        Returns:
        - bool: True if the filename is valid, False otherwise.
        """
        try:
            regex = re.compile(r"^[a-zA-Z0-9]([a-zA-Z0-9_ -]*[a-zA-Z0-9])?$")
            if not regex.match(self.name.get()):
                messagebox.showerror("Error", "Filename must begin and end with alphanumeric characters. "
                                              "Only whitespaces, hyphens, and underscores are allowed in "
                                              "between.")
                self.name_entry.focus_set()
                return False
            return True
        except (ValueError, tk.TclError):
            messagebox.showerror("Error", "Filename must begin and end with alphanumeric characters. "
                                          "Only whitespaces, hyphens, and underscores are allowed in "
                                          "between.")
            self.name_entry.focus_set()
            return False


def main():
    # Determine icon path
    base_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    icon_path = os.path.join(base_dir, "images", "icon.ico")

    # Setup window
    window = TKMT.ThemedTKinterFrame("Random Walk Simulation", "azure", "light")
    window.root.iconbitmap(icon_path)

    # Instantiate app
    App(window.root)

    # Run
    window.root.mainloop()


if __name__ == "__main__":
    main()
