import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import os
import argparse

# コマンドライン引数
parser = argparse.ArgumentParser(description='Real-time GNSS constellation plot.')
parser.add_argument('--prn', default='12', help='PRN number to plot')
parser.add_argument('--interval', type=int, default=500, help='Update interval (ms)')
parser.add_argument('--max-points', type=int, default=100000, help='Max points to plot')
parser.add_argument('--save', action='store_true', help='Save animation as MP4')
args = parser.parse_args()

filename = f'tracking_PRN_{args.prn}.dat'
last_size = 0  # ファイルサイズ追跡

fig, ax = plt.subplots(figsize=(6, 6))
scat = ax.scatter([], [], s=1, alpha=0.5, color='blue')
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 1.5)
ax.set_xlabel('I (同相成分)')
ax.set_ylabel('Q (直交位相成分)')
ax.set_title(f'Live Constellation (PRN {args.prn})')
ax.grid(True)
ax.axis('equal')

def update(frame):
    global last_size
    if not os.path.exists(filename):
        ax.set_title(f'PRN {args.prn} (ファイルなし)')
        return scat,

    try:
        # 新しいデータのみ読み込み
        current_size = os.path.getsize(filename)
        if current_size <= last_size:
            return scat,
        data = np.fromfile(filename, dtype=np.complex64, offset=last_size)
        last_size = current_size

        if len(data) == 0:
            ax.set_title(f'PRN {args.prn} (データなし)')
            return scat,

        # データ正規化
        power = np.mean(np.abs(data)**2)
        if power > 0:
            data = data / np.sqrt(power)
        else:
            ax.set_title(f'PRN {args.prn} (パワー0)')
            return scat,

        # データ量制限
        data = data[-args.max_points:]
        scat.set_offsets(np.c_[data.real, data.imag])
        ax.set_title(f'Live Constellation (PRN {args.prn}) - {len(data)} points')
    except Exception as e:
        print(f"Read error: {e}")
        ax.set_title(f'PRN {args.prn} (読み込みエラー)')
    return scat,

ani = FuncAnimation(fig, update, interval=args.interval)
if args.save:
    ani.save('constellation.mp4', writer='ffmpeg', dpi=300)
plt.show()
