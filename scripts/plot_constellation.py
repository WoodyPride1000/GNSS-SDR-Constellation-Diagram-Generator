import numpy as np
import matplotlib.pyplot as plt
import glob
import os

def plot_constellation(file_path, ax):
    """
    指定されたファイルからI/Qデータを読み込み、コンスタレーション図をプロットします。
    データは正規化され、見やすいように軸の範囲が固定されます。
    """
    if not os.path.exists(file_path):
        print(f"エラー: ファイルが見つかりません - {file_path}")
        # ファイルがない場合はサブプロットを非表示にし、タイトルにメッセージを表示
        ax.set_title(f"ファイルなし: {os.path.basename(file_path)}")
        ax.axis('off')
        return

    data = np.fromfile(file_path, dtype=np.complex64)
    
    # ファイル名からPRN番号を抽出
    prn = file_path.split('_')[-1].split('.')[0]

    if len(data) == 0:
        print(f"警告: データが空です - {file_path}")
        ax.set_title(f'PRN {prn} (データなし)')
        ax.axis('off') # データがない場合はプロット自体を非表示にする
        return

    # --- 改善点1: I/Qデータの正規化 ---
    # データの振幅を平均パワーで正規化することで、異なるPRN間の比較が容易になります。
    # 理想的なBPSK信号の振幅が約1になるように調整します。
    power = np.mean(np.abs(data)**2)
    if power > 0:
        data_normalized = data / np.sqrt(power)
    else:
        # パワーが0の場合は正規化できないため、そのままプロット
        print(f"警告: PRN {prn} のパワーが0です。正規化せずにプロットします。")
        data_normalized = data

    ax.scatter(data_normalized.real, data_normalized.imag, s=1, alpha=0.5)
    
    ax.set_title(f'PRN {prn}')
    ax.set_xlabel('I (同相成分)')
    ax.set_ylabel('Q (直交位相成分)')
    
    # --- 改善点2: 軸の範囲を固定 ---
    # 全てのプロットで同じI/Q範囲を使うことで、散らばり具合を直接比較できます。
    # 正規化後のBPSK信号であれば、±1.5程度の範囲が適切です。
    ax.set_xlim([-1.5, 1.5])
    ax.set_ylim([-1.5, 1.5])
    
    ax.axis('equal') # I軸とQ軸のスケールを同じにする
    ax.grid(True)

# GNSS-SDRが出力する追尾データファイルを探す
# 例: tracking_PRN_01.dat, tracking_PRN_02.dat など
tracking_files = glob.glob('tracking_PRN_*.dat')
tracking_files.sort() # PRN順に並べ替える

if not tracking_files:
    print("指定されたパターン 'tracking_PRN_*.dat' に一致するファイルが見つかりませんでした。")
    print("GNSS-SDRの設定と出力ファイル名を確認してください。")
else:
    # サブプロットのレイアウトを動的に決定
    num_files = len(tracking_files)
    cols = 3 # 1行あたりのプロット数
    rows = (num_files + cols - 1) // cols # 必要な行数を計算
    
    fig, axs = plt.subplots(rows, cols, figsize=(5 * cols, 5 * rows))
    # axsが2次元配列の場合があるので、1次元に平坦化
    axs = axs.flatten()

    # 各ファイルをループしてプロット
    for i, file in enumerate(tracking_files):
        plot_constellation(file, axs[i])
    
    # --- 改善点3: 余分なサブプロットを非表示にする処理 ---
    # 検出されたファイル数より多いサブプロットがある場合、それらを非表示にします。
    for j in range(num_files, len(axs)):
        axs[j].axis('off')

    plt.tight_layout() # サブプロット間のスペースを自動調整
    plt.show()
