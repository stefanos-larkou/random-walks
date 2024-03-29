from itertools import product
import matplotlib.pyplot as plt
import numpy as np
from typing import List, Tuple, Optional


class RandomWalker:
    """
    A class for simulating a random walker.

    Parameters:
    - start (Tuple[float, ...]): The starting position of the walker.
    - ndim (Optional[int]):      The number of dimensions for the walker. Default is 1. Must be between 1 and 3
                                 inclusive.
    - seed (Optional[int]):      The random seed for reproducibility. Default is -1, indicating no seed.

    Attributes:
    - ndim (int):                                      The number of dimensions the walker can move in.
    - track_data (List[Tuple[Tuple[float, ...], float, float]]):
                                                       A list containing information about the walker's position,
                                                       distance from the start, and distance from the origin during each
                                                       step.
    - start (np.ndarray):                              The starting position of the walker.
    - offsets (List[Tuple[int, ...]]):                 The possible step offsets in each dimension.
    - line (matplotlib.lines.Line2D):                  The line to be plotted. It is none until plot_track() is called.
    - markers (matplotlib.collections.PathCollection): The scatter points to be plotted. None until plot_track() is
                                                       called.

    Methods:
    - random_step(position: Tuple[float, ...]) -> Tuple[float, ...]:
                                                         Take a random step from the current position.
    - distance_from_start(position: Tuple[float, ...]) -> float:
                                                         Calculate the Euclidean distance from the start position.
    - distance_from_origin(position: Tuple[float, ...]) -> float:
                                                         Calculate the Euclidean distance from the origin.
    - random_walk(nstep: int) -> None:                   Simulate a random walk for a given number of steps.
    - track() -> List[Tuple[float, ...]]:                Get a list of positions visited during the random walk.
    - plot_track(ax: Optional[plt.Axes] = None) -> None: Plot the walker's position during each step.
    """
    def __init__(self, start: Tuple[float, ...], ndim: Optional[int] = 1, allow_diagonals: Optional[bool] = False, seed: Optional[int] = -1) -> None:
        """
        Initialise the RandomWalker object.

        Parameters:
        - start (Tuple[float, ...]):        The starting position of the walker.
        - ndim (Optional[int]):             The number of dimensions for the walker. Default is 1, must be between 1 and
                                            3 inclusive.
        - allow_diagonals (Optional[bool]): Whether to allow diagonal movements. Default is False.
        - seed (Optional[int]):             The random seed for reproducibility. Default is -1, indicating no seed.

        Attributes:
        - ndim (int):                      The number of dimensions the walker can move in.
        - start (np.ndarray):              The starting position of the walker.
        - offsets (List[Tuple[int, ...]]): The possible step offsets in each dimension.
        - track_data (List[Tuple[Tuple[float, ...], float, float]]):
                                           A list containing information about the walker's position, distance from the
                                           starting position, and distance from the origin during each step.
        """
        # Set dimensionality and check if it is valid
        self.ndim = ndim
        self._check_valid_dimensionality()

        # Set start position and add first point to track
        self.track_data = []
        self.start = np.asarray(start)
        self.track_data.append((start, self.distance_from_origin(start), 0.))

        # Initialise line for plotting
        self.line = None
        self.markers = None

        # Set seed if given
        if seed > 0:
            np.random.seed(seed)

        # Set possible movements of the random walk
        if allow_diagonals:
            self.offsets = list(product([-1, 0, 1], repeat=self.ndim))
            self.offsets.remove(tuple([0] * self.ndim))
        else:
            self.offsets = [tuple([0 if j != i else direction for j in range(self.ndim)]) for direction in [1, -1] for i in range(self.ndim)]

    def _check_valid_position(self, position: Tuple[float, ...]) -> None:
        """
        Check if the given position has the correct dimensionality.

        Parameters:
        - position (Tuple[float, ...]): The position to check.

        Raises:
        - ValueError: If the position has an incorrect dimensionality.
        """
        if len(position) != self.ndim:
            raise ValueError(f"Unexpected dimensionality for position. Expected {self.ndim} dimensions, but {position} \
                               has {len(position)}.")

    def _check_valid_dimensionality(self) -> None:
        """
        Check if the number of dimensions of the object is between 1 and 3 inclusive.

        Raises:
        - ValueError: If the number of dimensions of the object is not between 1 and 3 inclusive.
        """
        if not 1 <= self.ndim <= 3:
            raise ValueError("Invalid value for ndim. The number of dimensions must be between 1 and 3 (inclusive).")

    def random_step(self, position: Tuple[float, ...]) -> Tuple[float, ...]:
        """
        Take a random step from the given position.

        Parameters:
        - position (Tuple[float, ...]): The current position.

        Returns:
        - Tuple[float, ...]: The new position after taking a random step.
        """
        offset = self.offsets[np.random.choice(len(self.offsets))]
        newstep = tuple(p + o for p, o in zip(position, offset))
        return newstep

    def distance_from_start(self, position: Tuple[float, ...]) -> float:
        """
        Calculate the Euclidean distance from the start position.

        Parameters:
        - position (Tuple[float, ...]): The position to calculate the distance from.

        Returns:
        - float: The Euclidean distance from the start position.
        """
        self._check_valid_position(position)
        distance = np.sqrt(np.sum((self.start - np.asarray(position)) ** 2))
        return distance

    def distance_from_origin(self, position: Tuple[float, ...]) -> float:
        """
        Calculate the Euclidean distance from the origin.

        Parameters:
        - position (Tuple[float, ...]): The position to calculate the distance from.

        Returns:
        - float: The Euclidean distance from the origin.
        """
        self._check_valid_position(position)
        distance = np.sqrt(np.sum((np.asarray((0,) * self.ndim) - np.asarray(position)) ** 2))
        return distance

    def random_walk(self, nstep: int) -> None:
        """
        Simulate a random walk for a given number of steps.

        Parameters:
        - nstep (int): The number of steps to simulate.
        """
        # Start from given starting position and perform nstep steps
        current = tuple(self.start)
        for i in range(nstep):
            # Take a step to get new position
            current = self.random_step(current)

            # Calculate distance from origin and starting point
            dist_origin = self.distance_from_origin(current)
            dist_start = self.distance_from_start(current)

            # Add step and distances to track
            self.track_data.append((current, dist_origin, dist_start))

    def track(self) -> List[Tuple[float, ...]]:
        """
        Get a list of positions visited during the random walk.

        Returns:
        - List[Tuple[float, ...]]: List of positions visited during the random walk.
        """
        return [tr[0] for tr in self.track_data]

    def plot_track(self, ax: Optional[plt.Axes] = None, frame: Optional[int] = None) -> None:
        """
        Plot the walker's position during each step.

        - ax (Optional[plt.Axes]):      The axes on which to plot. Default is None. If None, a new subplot will be
                                        created.
        - frame (Optional[int]):        The current animation frame number. Default is None. If None, it is assumed that
                                        the entire plot is being plotted. If a number is given, the positions visited
                                        during the random walk are cut off up until the corresponding index so that each
                                        step of the animation plots the correct number of points.
        """
        # If no axis is given to plot on create one
        if ax is None:
            fig = plt.figure()
            ax = fig.add_subplot(111, projection="3d") if self.ndim == 3 else fig.add_subplot(111)

        # Get all past positions of the random walk
        positions = self.track()

        if self.ndim == 1:
            # Unpack positions
            x = [pos[0] for pos in positions]

            # Filter positions by frame if animating
            if frame is not None:
                x = x[:frame + 1]

            # If no line is already present, create it
            if self.line is None:
                self.line, = ax.plot([], [], alpha=0.7)

            # If no markers are already present, create them
            if self.markers is None:
                self.markers = ax.scatter([], [], color='r', marker='D', s=8, alpha=0.2)

            # Update the line and markers with the new positions
            self.line.set_data(range(len(x)), x)
            self.markers.set_offsets(np.column_stack([range(len(x)), x]))
        elif self.ndim == 2:
            # Unpack positions
            x, y = zip(*positions)

            # Filter positions by frame if animating
            if frame is not None:
                x, y = x[:frame + 1], y[:frame + 1]

            # If no line is already present, create it
            if self.line is None:
                self.line, = ax.plot([], [], alpha=0.7)

            # If no markers are already present, create them
            if self.markers is None:
                self.markers = ax.scatter([], [], color='r', marker='D', s=8, alpha=0.2)

            # Update the line and markers with the new positions
            self.line.set_data(x, y)
            self.markers.set_offsets(np.column_stack([x, y]))
        elif self.ndim == 3:
            # Unpack positions
            x, y, z = zip(*positions)

            # Filter positions by frame if animating
            if frame is not None:
                x, y, z = x[:frame + 1], y[:frame + 1], z[:frame + 1]

            # If no line is already present, create it
            if self.line is None:
                self.line, = ax.plot([], [], alpha=0.7)

            # Update the line with the new positions
            self.line.set_data_3d(x, y, z)
