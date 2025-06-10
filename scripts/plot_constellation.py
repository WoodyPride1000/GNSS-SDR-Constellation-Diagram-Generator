import numpy as np
import matplotlib.pyplot as plt
import glob
import os

def plot(file, ax):
    if not os.path.exists(file):
        print(f"Missing: {file}")
        return
    data = np.fromfile(file, dtype=np.complex64)
    ax.scatter(data.real, data.imag, s=1, alpha=0.5)
    prn = file.split('_')[-1].split('.')[0]
    ax.set_title(f'PRN {prn}')
    ax.set_xlabel('I')
    ax.set_ylabel('Q')
    ax.axis('equal')
    ax.grid(True)

files = glob.glob('tracking_PRN_*.dat')
cols = 3
rows = (len(files) + cols - 1) // cols
fig, axs = plt.subplots(rows, cols, figsize=(5*cols, 5*rows))
axs = axs.flatten()

for i, file in enumerate(files):
    plot(file, axs[i])
for j in range(i+1, len(axs)):
    axs[j].axis('off')

plt.tight_layout()
plt.show()
