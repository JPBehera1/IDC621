import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# What I did with my code here is, grains after toppling are not just limited to their neighbouring cells but also oscillate between other cells and the neighbouring cells
GRID_SIZE = 50  
THRESHOLD = 4   
DECAY = 0.95    # Like all true oscillations, DECAY is the damping in the oscillation


grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=float)
velocity = np.zeros_like(grid)  

toppling_counts = []
avalanche_counts = []

# Adding grains
def add_sand(grid):
    for _ in range(10):  
        x, y = np.random.randint(0, GRID_SIZE, size=2)  
        grid[x, y] += 1  

# Function to apply harmonic dynamics during toppling
def topple(grid, velocity):
    toppling_count = 0  # Count of topplings in this generation
    while (grid >= THRESHOLD).any():  # Continue until no cell exceeds threshold
        toppling_cells = np.argwhere(grid >= THRESHOLD)  # Find all cells that need to topple
        for x, y in toppling_cells:
            grid[x, y] -= 4  # Remove 4 grains from the toppling cell
            velocity[x, y] = -velocity[x, y] * DECAY  # Harmonic dynamics (optional)
            toppling_count += 1  # Count this toppling

            # Distribute grains to neighbors
            if x > 0: grid[x - 1, y] += 1  # Top neighbor
            if x < GRID_SIZE - 1: grid[x + 1, y] += 1  # Bottom neighbor
            if y > 0: grid[x, y - 1] += 1  # Left neighbor
            if y < GRID_SIZE - 1: grid[x, y + 1] += 1  # Right neighbor

    return toppling_count

def update(frameNum, img, grid, velocity):
    add_sand(grid)  
    toppling_count = topple(grid, velocity)
    toppling_counts.append(toppling_count)
    avalanche_counts.append(1 if toppling_count > 0 else 0)
    grid += velocity  
    velocity *= DECAY  
    img.set_data(grid) 
    return img,

fig, ax = plt.subplots()
img = ax.imshow(grid, cmap='inferno', interpolation='nearest', vmin=0, vmax=THRESHOLD-1)

ani = animation.FuncAnimation(fig, update, fargs=(img, grid, velocity), frames=1000, interval=200, blit=False, repeat=False)
plt.show()


plt.figure(figsize=(10, 6))

# Plot toppling counts
plt.subplot(2, 1, 1)
plt.plot(toppling_counts, label='Topplings per Generation', color='blue')
plt.ylabel('Topplings')
plt.title('Number of Topplings per Generation')
plt.legend()

# Plot avalanche counts
plt.subplot(2, 1, 2)
plt.plot(avalanche_counts, label='Avalanches per Generation', color='red')
plt.xlabel('Generation')
plt.ylabel('Avalanches')
plt.title('Number of Avalanches per Generation')
plt.legend()

total_topplings = np.cumsum(toppling_counts)  
total_avalanches = np.cumsum(avalanche_counts)

#This line of code is to avoid log(0) error 
nonzero_topplings = total_topplings[total_topplings > 0]
nonzero_avalanches = total_avalanches[total_avalanches > 0]

plt.subplot(3, 1, 3)
plt.loglog(nonzero_topplings, nonzero_avalanches, label='Log-Log Topplings vs Avalanches', color='green')
plt.xlabel('Log(Total Topplings)')
plt.ylabel('Log(Total Avalanches)')
plt.title('Log-Log Plot of Topplings vs Avalanches')
plt.legend()

plt.tight_layout()
plt.show()





