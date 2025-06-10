import numpy as np
import matplotlib.pyplot as plt
import glob
import os
import argparse

def plot_constellation(file_path, ax, color, index):
    """
    指定されたファイルからI/Qデータを読み込み、コンスタレーション図をプロットします。
    データは正規化され、軸範囲は固定。エラーハンドリングを強化。
    """
    if not os.path.exists(file_path):
        print(f"エラー: ファイルが見つかりません - {file_path}")
        ax.set_title(f"ファイルなし: {os.path.basename(file_path)}")
        ax.axis('off')
        return

    # ファイル名からPRN番号を抽出
    prn = file_path.split('_')[-1].split('.')[0]

    try:
        # メモリ効率のために最大サンプル数を制限
        max_samples = 10000
        data = np.fromfile(file_path, dtype=np.complex64)
        if len(data) > max_samples:
            data = data[:max_samples]
    except Exception as e:
        print(f"エラー: ファイル読み込みに失敗しました - {file_path} ({e})")
        ax.set_title(f'PRN {prn} (読み込み失敗)')
        ax.axis('off')
        return

    if len(data) == 0:
        print(f"警告: データが空です - {file_path}")
        ax.set_title(f'PRN {prn} (データなし)')
        ax.axis('off')
        return

    # データ正規化
    power = np.mean(np.abs(data)**2)
    if power > 0:
        data_normalized = data / np.sqrt(power)
    else:
        print(f"エラー: PRN {prn} のパワーが0です。プロットをスキップします。")
        ax.set_title(f'PRN {prn} (パワー0)')
        ax.axis('off')
        return

    # プロット
    s = max(1, 5000 / len(data_normalized))  # 動的マーカーサイズ
    ax.scatter(data_normalized.real, data_normalized.imag, s=s, alpha=0.5, color=color)
    ax.set_title(f'PRN {prn}')
    ax.set_xlabel('I (同相成分)')
    ax.set_ylabel('Q (直交位相成分)')
    ax.set_xlim([-1.5, 1.5])
    ax.set_ylim([-1.5, 1.5])
    ax.axis('equal')
    ax.grid(True)

def main():
    # コマンドライン引数
    parser = argparse.ArgumentParser(description='Plot GNSS constellation diagrams.')
    parser.add_argument('--path', default='.', help='Directory containing tracking files')
    parser.add_argument('--save', action='store_true', help='Save plot as PNG')
    args = parser.parse_args()

    # トラッキングファイルを取得
    tracking_files = glob.glob(os.path.join(args.path, 'tracking_PRN_*.dat'))
    tracking_files.sort()

    if not tracking_files:
        print("指定されたパターン 'tracking_PRN_*.dat' に一致するファイルが見つかりませんでした。")
        print("GNSS-SDRの設定と出力ファイル名を確認してください。")
        return

    # サブプロットレイアウト
    num_files = min(len(tracking_files), 12)  # 最大12プロット
    cols = 3
    rows = (num_files + cols - 1) // cols
    fig, axs = plt.subplots(rows, cols, figsize=(5 * cols, 5 * rows))
    axs = axs.flatten()

    # 色設定
    colors = plt.cm.tab10(np.linspace(0, 1, 10))

    # プロット
    for i, file in enumerate(tracking_files[:num_files]):
        plot_constellation(file, axs[i], colors[i % 10], i)

    # 余分なサブプロットを非表示
    for j in range(num_files, len(axs)):
        axs[j].axis('off')

    plt.tight_layout()
    if args.save:
        plt.savefig('constellation.png', dpi=300, bbox_inches='tight')
        print("プロットを 'constellation.png' に保存しました。")
    plt.show()

if __name__ == "__main__":
    main()
