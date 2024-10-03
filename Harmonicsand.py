import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Parameters for the sandpile simulation
GRID_SIZE = 50  # Grid dimensions (GRID_SIZE x GRID_SIZE)
THRESHOLD = 3   # Sand threshold for toppling
DECAY = 1    # Damping factor for harmonic oscillation

# Initialize the grid with zeros (sand distribution) and velocities for harmonic oscillations
grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=float)
velocity = np.zeros_like(grid)  # Velocity grid to simulate harmonic dynamics

# Function to add a grains of sand at a random location
def add_sand(grid):
    for _ in range(10):  # Loop to add five grains
        x, y = np.random.randint(0, GRID_SIZE, size=2)  # Random location on the grid
        grid[x, y] += 1  # Add one grain of sand at the random location

# Function to apply harmonic dynamics during toppling
def harmonic_topple(grid, velocity):
    avalanche = False
    while np.any(grid >= THRESHOLD):  # While there are cells above the threshold
        avalanche = True
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if grid[i, j] >= THRESHOLD:
                    grid[i, j] -= THRESHOLD  # Reduce sand at the current cell by 4
                    velocity[i, j] = -velocity[i, j] * DECAY  # Flip velocity and apply damping
                    
                    if i > 0:  # Topple to the cell above with harmonic influence
                        grid[i-1, j] += 1
                        velocity[i-1, j] += 0.25 * velocity[i, j]  # Propagate velocity
                    
                    if i < GRID_SIZE-1:  # Topple to the cell below with harmonic influence
                        grid[i+1, j] += 1
                        velocity[i+1, j] += 0.25 * velocity[i, j]
                    
                    if j > 0:  # Topple to the cell on the left with harmonic influence
                        grid[i, j-1] += 1
                        velocity[i, j-1] += 0.25 * velocity[i, j]
                    
                    if j < GRID_SIZE-1:  # Topple to the cell on the right with harmonic influence
                        grid[i, j+1] += 1
                        velocity[i, j+1] += 0.25 * velocity[i, j]
    return avalanche
"""  """
# Function to update the grid and animation
def update(frameNum, img, grid, velocity):
    add_sand(grid)  # Add sand at a random location
    avalanche_occurred = harmonic_topple(grid, velocity)  # Check for and perform topples with harmonic dynamics
    grid += velocity  # Apply velocity to the grid (wave-like behavior)
    velocity *= DECAY  # Apply damping to the velocities
    img.set_data(grid)  # Update the grid image
    return img,

# Visualization using Matplotlib animation
fig, ax = plt.subplots()
# Using 'coolwarm' colormap for harmonic effects (negative/positive dynamics)
img = ax.imshow(grid, cmap='Blues', interpolation='nearest', vmin=-THRESHOLD, vmax=THRESHOLD)

ani = animation.FuncAnimation(fig, update, fargs=(img, grid, velocity), frames=10000, interval=200, repeat=False)

plt.colorbar(img)
plt.title("Lmao")
plt.show()