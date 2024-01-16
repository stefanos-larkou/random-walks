# Random Walk Simulation

Implement random walk simulations using Python. The simulations allow users to visualize the paths of multiple random walks in one, two, or three dimensions. They can be run as an animation or as a static plot.

<div align=center style="display: flex; justify-content: center; gap: 1%;">
  <img src="readme_gifs/readme_1d.gif" alt="Random Walk 1D GIF" width="30%">
  <img src="readme_gifs/readme_2d.gif" alt="Random Walk 2D GIF" width="30%">
  <img src="readme_gifs/readme_3d.gif" alt="Random Walk 3D GIF" width="30%">
</div>

## Table of Contents
- [Project Structure](#project-structure)
  - [Folders](#folders)
  - [Files](#files)
- [Usage](#usage)
  - [Main Program](#main-program)
  - [Executable](#executable)
  - [Examples](#examples)
- [Dependencies](#dependencies)
- [License](#license)

## Project Structure

```
Root Directory
├── images
│   └── icon.ico
│
└── src
    ├── examples
    │   ├── animation_example.py
    │   └── plot_examples.py
    ├── main.py
    ├── random_walker.py
    └── visualisation.py
```

### Folders
- **images**: The GUI's icon is located here. More importantly, when saving a plot, it is placed in a subdirectory that will be created here.
<br> _Note_: If running the executable, a new directory will be created in the same folder containing the newly saved file.
- **src**: The source code folder.
- **examples**: The scripts that demonstrate how to use the RandomWalker class and plot the results are located here.

### Files
- **random_walker.py**: Contains the `RandomWalker` class, which is used for simulating a random walk. This class is used in all other files.
- **animation_example.py**: Example script demonstrating the animation of random walks. The global configuration variables can be modified to change the properties of the simulation.
- **plot_examples.py**: Example script demonstrating static plots of random walks. The global configuration variables can be modified to change the properties of the simulation.
- **visualisation.py**: Contains functions for setting up the Matplotlib axes, plotting animations and static plots.
- **main.py**: The main script. It includes a simple GUI built with tkinter for configuring and running the simulation.

## Usage
### Main Program
1. Run `main.py` to launch the GUI.
2. Configure the simulation parameters.
3. Click on the "Run Simulations" button.
4. The animation or static plot of the simulation will appear.

### Executable
1. Open RWalk.exe
2. Configure the simulation parameters using the provided inputs.
3. Click on the "Run Simulations" button.
4. The animation or static plot of the simulation will appear.

### Examples
1. Open `animation_example.py` or `plot_examples.py`
2. Configure the simulation parameters by adjusting the global variables.
3. Run the script. 
4. A new window will pop up with the animation or static plot of the simulation.

## Dependencies

On top of Python, the project relies on the following external libraries:

- **Matplotlib**: Used for creating the plots.
- **NumPy**: Used for numerical operations and data structuring.
- **TKinterModernThemes**: Used to give the tkinter GUI a nicer look.

To install the dependencies, you can use the following command:

```bash
pip install -r requirements.txt
```

To install python, see the [official website](https://www.python.org/downloads/)
<br> _Note_: This application was built on Python 3.11.

## License

This project is licensed under the MIT License - see the [license](LICENSE.md) file for details.
