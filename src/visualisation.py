import matplotlib.lines
import mpl_toolkits.mplot3d as p3
import mpl_toolkits.mplot3d.art3d
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from typing import List, Union, Optional
from random_walker import RandomWalker
from typing import Tuple
import os

matplotlib.use("TkAgg")


def setup_axes(ndim: int) -> Tuple[plt.Figure, Union[plt.Axes, p3.axes3d.Axes3D]]:
    """
    Set up the Matplotlib figure and axes for plotting random walks.

    Parameters:
    - ndim (int): The number of dimensions for the walkers.

    Returns:
    - Tuple[plt.Figure, Union[plt.Axes, p3.axes3d.Axes3D]]: The created figure and axes to plot on.
    """
    # Instantiate plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d") if ndim == 3 else fig.add_subplot(111)

    # Set title and labels
    ax.set_title(f"Random Walk - {ndim}D")
    if ndim == 1:
        ax.set_xlabel("Step")
        ax.set_ylabel("x")
    elif ndim == 2:
        ax.set_xlabel("x")
        ax.set_ylabel("y")
    elif ndim == 3:
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_zlabel("z")

    return fig, ax


def set_ax_lims(rwalkers: List[RandomWalker], ax: Union[plt.Axes, p3.axes3d.Axes3D], ndim: int, nsteps: int, frame: Optional[int] = None) -> None:
    """
    Set the axes limits of the plot.

    Parameters:
    - rwalkers (List[RandomWalker]): List of RandomWalker instances which will be visualised.
    - ax (Union[plt.Axes, p3]):      The axes on which to plot.
    - ndim (int):                    The number of dimensions for the walkers.
    - nsteps (int):                  The number of steps in each random walk.
    - frame (Optional[int]):         The current frame number. Defaults to None. If none, all positions will be used
                                     when determining the axes limits.
    """
    # If not animating then take all positions
    if frame is None:
        frame = nsteps

    # Get list of positions for each walker
    positions = [rwalker.track()[:frame + 1] for rwalker in rwalkers]

    if ndim == 1:
        # Place the x values of all walkers in a list
        x = [p[0] for pos in positions for p in pos]

        # x-axis depends on the number of steps, y-axis on maximum and minimum of the x values
        ax.set_xlim(0, frame + 1)
        ax.set_ylim(min(x) - 1, max(x) + 1)
    elif ndim == 2:
        # Place the x, y values of all walkers in lists
        x = [p[0] for pos in positions for p in pos]
        y = [p[1] for pos in positions for p in pos]

        # x-axis depends on maximum and minimum of the x values,
        # y-axis on maximum and minimum of the y values
        ax.set_xlim(min(x) - 1, max(x) + 1)
        ax.set_ylim(min(y) - 1, max(y) + 1)
    elif ndim == 3:
        # Place the x, y, z values of all walkers in lists
        x = [p[0] for pos in positions for p in pos]
        y = [p[1] for pos in positions for p in pos]
        z = [p[2] for pos in positions for p in pos]

        # x-axis depends on maximum and minimum of the x values,
        # y-axis on maximum and minimum of the y values,
        # z-axis on maximum and minimum of the z values
        ax.set_xlim(min(x) - 1, max(x) + 1)
        ax.set_ylim(min(y) - 1, max(y) + 1)
        ax.set_zlim(min(z) - 1, max(z) + 1)


def save_fig(fig: plt.Figure, ndim: int, name: str) -> None:
    """
    Save the resulting figure to a file.

    Parameters:
    - fig (plt.Figure): The final figure to be saved.
    - ndim (int):       The number of dimensions of the random walks, used for determining the directory name.
    - name (str):       The filename.
    """
    path = f"images/plots{ndim}d"
    os.makedirs(path, exist_ok=True)
    fig.savefig(os.path.join(path, f"{name}.png"), dpi=200)


def update(frame: int, ax: Union[plt.Axes, p3.axes3d.Axes3D], rwalkers: List[RandomWalker], stable_lims: bool, ndim: int, nsteps: int) -> List[Union[matplotlib.lines.Line2D, mpl_toolkits.mplot3d.art3d.Line3D]]:
    """
    Update function for the animation. Called by Matplotlib's FuncAnimation to update the plot for each frame of the
    animation.

    Parameters:
    - frame (int):                            The current animation frame number.
    - ax (Union[plt.Axes, p3.axes3d.Axes3D]): The axes on which to plot.
    - rwalkers (List[RandomWalker]):          List of RandomWalker instances to visualize.
    - stable_lims (bool):                     Whether to keep the axes limits constant when animating or not.
    - ndim (int):                             The number of dimensions for the walkers.
    - nsteps (int):                           The number of steps in each random walk.

    Returns:
    - List[Union[matplotlib.lines.Line2D, mpl_toolkits.mplot3d.art3d.Line3D]]: List of artists representing the plotted
                                                                               elements.
    """
    artists = []

    for rwalker in rwalkers:
        rwalker.plot_track(ax, frame)
        artists.extend(ax.lines)

    if not stable_lims:
        set_ax_lims(rwalkers, ax, ndim, nsteps, frame)

    return artists


def run_animation(rwalkers: List[RandomWalker], ndim: int, nsteps: int, stable_lims: bool, save: bool, name: str) -> Tuple[FuncAnimation, plt.Figure]:
    """
    Run the animation of random walker simulations.

    Parameters:
    - rwalkers (List[RandomWalker]): List of RandomWalker instances to visualize.
    - ndim (int):                    The number of dimensions for the walkers.
    - nsteps (int):                  The number of steps in each random walk.
    - stable_lims (bool):            Whether to keep the axes limits constant when animating or not.
    - save (bool):                   Whether to save the resulting figure to a file.
    - name (string):                 Name of the file to save

    Returns:
    Tuple[FuncAnimation, plt.Figure]: The animation object and the figure where it is plotted.
    """
    fig, ax = setup_axes(ndim)

    if stable_lims:
        set_ax_lims(rwalkers, ax, ndim, nsteps)

    # Run the animation
    animation = FuncAnimation(
        fig,
        update,
        fargs=(ax, rwalkers, stable_lims, ndim, nsteps),
        frames=nsteps,
        interval=min(1 / (nsteps * 2), 0.5),
        repeat=False
    )

    if save:
        save_fig(fig, ndim, name)

    return animation, fig


def run_plot(rwalkers: List[RandomWalker], ndim: int, nsteps: int, save: bool, name: str) -> plt.Figure:
    """
    Create a static plot of the random walks.

    Parameters:
    - rwalkers (List[RandomWalker]): List of RandomWalker instances to visualize.
    - ndim (int):                    The number of dimensions for the walkers.
    - nsteps (int):                  The number of steps in each random walk.
    - save (bool):                   Whether to save the resulting figure to a file.
    - name (string):                 Name of the file to save

    Returns:
    - plt.Figure:                    The figure containing the resulting plot.
    """
    fig, ax = setup_axes(ndim)
    set_ax_lims(rwalkers, ax, ndim, nsteps)

    for rwalker in rwalkers:
        rwalker.plot_track(ax)

    if save:
        save_fig(fig, ndim, name)

    return fig
