import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import os

filename = 'tracking_PRN_12.dat'

fig, ax = plt.subplots(figsize=(6,6))
scat = ax.scatter([], [], s=1, alpha=0.5)
ax.set_xlim(-1, 1)
ax.set_ylim(-1, 1)
ax.set_xlabel('I')
ax.set_ylabel('Q')
ax.set_title('Live Constellation (PRN 12)')
ax.grid(True)
ax.axis('equal')

def update(frame):
    if not os.path.exists(filename):
        return scat,
    try:
        data = np.fromfile(filename, dtype=np.complex64)
        if len(data) == 0:
            return scat,
        # データ量制限（最新10万点）
        data = data[-100000:]
        scat.set_offsets(np.c_[data.real, data.imag])
    except Exception as e:
        print(f"Read error: {e}")
    return scat,

ani = FuncAnimation(fig, update, interval=1000)
plt.show()
