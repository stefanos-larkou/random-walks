import matplotlib.pyplot as plt
import numpy as np
from typing import List, Tuple, Optional


class RandomWalker:
    """
    A class for simulating a random walker in multiple dimensions.

    Parameters:
    - start (Tuple[float, ...]): The starting position of the walker.
    - ndim (Optional[int]):      The number of dimensions for the walker. Default is 1. Must be between 1 and 3
                                 inclusive.
    - seed (Optional[int]):      The random seed for reproducibility. Default is -1, indicating no seed.

    Attributes:
    - ndim (int):                      The number of dimensions the walker can move in.
    - track_data (List[Tuple[Tuple[float, ...], float, float]]):
                                       A list containing information about the walker's position, distance from the
                                       start, and distance from the origin during each step.
    - start (np.ndarray):              The starting position of the walker.
    - offsets (List[Tuple[int, ...]]): The possible step offsets in each dimension.
    - noffsets (int):                  The total number of possible step offsets.

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

    def __init__(self, start: Tuple[float, ...], ndim: Optional[int] = 1, seed: Optional[int] = -1) -> None:
        """
        Initialise the RandomWalker object.

        Parameters:
        - start (Tuple[float, ...]): The starting position of the walker.
        - ndim (Optional[int]):      The number of dimensions for the walker. Default is 1, must be between 1 and 3
                                     inclusive.
        - seed (Optional[int]):      The random seed for reproducibility. Default is -1, indicating no seed.
        """
        self.ndim = ndim
        self._check_valid_dimensionality()

        self.track_data = []

        pos = np.asarray(start)
        distance = np.sqrt(np.sum(pos ** 2))

        self.track_data.append((start, distance, 0.))
        self.start = np.asarray(start)

        if seed > 0:
            np.random.seed(seed)

        self.offsets = []
        for i in range(self.ndim):
            for direction in [1, -1]:
                offset = [0] * self.ndim
                offset[i] = direction
                self.offsets.append(tuple(offset))

        self.noffsets = len(self.offsets)

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

        p = self.start
        q = np.asarray(position)

        distance = np.sqrt(np.sum((p - q) ** 2))
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

        p = np.asarray((0,) * self.ndim)
        q = np.asarray(position)

        distance = np.sqrt(np.sum((p - q) ** 2))
        return distance

    def random_walk(self, nstep: int) -> None:
        """
        Simulate a random walk for a given number of steps.

        Parameters:
        - nstep (int): The number of steps to simulate.
        """

        current = tuple(self.start)
        for i in range(nstep):
            current = self.random_step(current)

            dist_origin = self.distance_from_origin(current)
            dist_start = self.distance_from_start(current)

            self.track_data.append((current, dist_origin, dist_start))

    def track(self) -> List[Tuple[float, ...]]:
        """
        Get a list of positions visited during the random walk.

        Returns:
        - List[Tuple[float, ...]]: List of positions visited during the random walk.
        """

        return [tr[0] for tr in self.track_data]

    def plot_track(self, ax: Optional[plt.Axes] = None) -> None:
        """
        Plot the walker's position during each step.

        - ax (Optional[plt.Axes]): The 3D axes on which to plot. If None, a new subplot will be created for 1D and 2D
                                   walks, and the default 3D subplot will be used for 3D walks.
        """
        positions = self.track()

        if self.ndim == 1:
            if ax is None:
                fig = plt.figure()
                ax = fig.add_subplot(111)

            positions = [pos[0] for pos in positions]
            ax.plot(range(len(positions)), positions, marker='o', markersize=1.5, alpha=0.4)
            ax.set_title('Random Walker 1D')
            ax.set_xlabel('Step')
            ax.set_ylabel('Position')
        elif self.ndim == 2:
            if ax is None:
                fig = plt.figure()
                ax = fig.add_subplot(111)

            x, y = zip(*positions)
            ax.plot(x, y, marker='o', markersize=1.5, alpha=0.4)
            ax.set_title('Random Walker 2D')
            ax.set_xlabel('X-axis')
            ax.set_ylabel('Y-axis')
        elif self.ndim == 3:
            if ax is None:
                fig = plt.figure()
                ax = fig.add_subplot(111, projection='3d')

            x, y, z = zip(*positions)
            ax.plot(x, y, z, marker='o', markersize=1.5, alpha=0.4)
            ax.set_title(f'Random Walker {self.ndim}D')
            ax.set_xlabel('X-axis')
            ax.set_ylabel('Y-axis')
            ax.set_zlabel('Z-axis')
