# A* Path Finding Algorithm Visualizer

This project is an implementation of the A* Path Finding Algorithm using the Pygame library to visualize the algorithm in real-time. The algorithm finds the shortest path between two points in a grid while avoiding obstacles.

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)

## Requirements

This project requires the following dependencies:

- Python 3.8+
- Pygame
- Poetry

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/bileshg/A-Star-Visualization.git
   ```
2. Change to the repository directory:
   ```bash
   cd A-Star-Visualization
   ```
3. Install [Poetry](https://python-poetry.org/docs/#installation) if you don't have it already.

4. Install the required dependencies using Poetry:
   ```bash
   poetry install
   ```

## Usage

1. Activate the virtual environment created by Poetry:
   ```bash
   poetry shell
   ```
2. Run the main.py file to launch the visualizer:
   ```bash
   python3 main.py
   ```
3. A window will open displaying an empty grid.

4. To start the visualization:
   - Left-click on the grid to create a <span style="color:red">start node</span> (first left-click), <span style="color:blue">end node</span> (second left-click), or barriers (subsequent left-clicks).
   - Right-click on any node to reset it to the default state.
   - Press the spacebar to begin the A* pathfinding algorithm visualization.
   - Press 'C' to clear the grid and start over.
