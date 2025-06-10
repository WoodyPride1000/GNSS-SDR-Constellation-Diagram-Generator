GNSS-SDR Constellation Diagram Generator
このリポジトリは、Software Defined Radio（SDR）を使用してGNSS信号（例: GPS L1 C/A）を受信し、GNSS-SDRで処理した後、復調データのコンスタレーション図をPythonで表示する手順を提供します。
前提条件
ハードウェア:
SDRデバイス（例: RTL-SDR）

GNSSアンテナ（L1バンド対応、1575.42 MHz）

ソフトウェア:
Ubuntu（推奨）

GNSS-SDR

Python 3（numpy, matplotlib）

RTL-SDRドライバ

依存ライブラリ:
bash

sudo apt-get install build-essential cmake git libboost-all-dev liblog4cpp5-dev libblas-dev liblapack-dev libarmadillo-dev libgnutls28-dev libpcap-dev libpugixml-dev libprotobuf-dev protobuf-compiler libuhd-dev
pip install numpy matplotlib

セットアップ
1. GNSS-SDRのインストール
bash

git clone https://github.com/gnss-sdr/gnss-sdr
cd gnss-sdr
mkdir build && cd build
cmake -DENABLE_GUI=OFF -DENABLE_VOLK=ON ..
make
sudo make install

2. RTL-SDRドライバのインストール
bash

sudo apt-get install rtl-sdr
rtl_test  # デバイス確認

信号取得と処理
1. GNSS信号のキャプチャ
RTL-SDRでGPS L1信号（1575.42 MHz）をキャプチャ。4 Msps以上を推奨。
bash

rtl_sdr -f 1575.42e6 -s 4e6 -g 20 -n 40000000 capture.dat

-s 4e6: 4 Msps（帯域幅2 MHzをカバー）

-g 20: ゲイン（rtl_sdr -gで利用可能な値を確認）

-n 40000000: 10秒分のサンプル（約1.9 GB）

注意: ディスク容量を確保（数GB必要）。

2. GNSS-SDRで信号処理
設定ファイル（front-end-cal.conf）を編集：
ini

[GNSS-SDR]
SignalSource.implementation=File_Signal_Source
SignalSource.filename=/path/to/capture.dat
SignalSource.sampling_frequency=4000000
SignalSource.item_type=gr_complex

[Tracking]
implementation=GPS_L1_CA_DLL_PLL_Tracking
dump=true
dump_filename=tracking.dat

実行：
bash

gnss-sdr --config_file=front-end-cal.conf

ログで衛星捕捉（PRN番号、C/N0値）を確認。C/N0 > 30 dB-Hzが目安。

コンスタレーション表示
1. I/Qデータ抽出
tracking.dat（またはtracking_PRN_XX.dat）にI/Qデータが保存される。

2. Pythonでプロット
以下のスクリプトでコンスタレーション図を表示：
python

import numpy as np
import matplotlib.pyplot as plt

# I/Qデータ読み込み
data = np.fromfile('tracking_PRN_12.dat', dtype=np.complex64)

# コンスタレーション図プロット
plt.figure(figsize=(6, 6))
plt.scatter(data.real, data.imag, s=1, alpha=0.5)
plt.title('GNSS Constellation Diagram (PRN 12)')
plt.xlabel('In-Phase (I)')
plt.ylabel('Quadrature (Q)')
plt.grid(True)
plt.axis('equal')
plt.show()

複数PRNのプロット
python

import numpy as np
import matplotlib.pyplot as plt
import glob

files = glob.glob('tracking_PRN_*.dat')
plt.figure(figsize=(10, 6))
for file in files:
    data = np.fromfile(file, dtype=np.complex64)
    prn = file.split('_')[-1].split('.')[0]
    plt.scatter(data.real, data.imag, s=1, alpha=0.5, label=f'PRN {prn}')

plt.title('GNSS Constellation Diagram (Multiple PRNs)')
plt.xlabel('In-Phase (I)')
plt.ylabel('Quadrature (Q)')
plt.grid(True)
plt.axis('equal')
plt.legend()
plt.show()

トラブルシューティング
コンスタレーションが散乱:
アンテナを空が広く見える場所に設置。

アクティブアンテナの場合、バイアスTを有効化（rtl_sdr -T）。

外部LNA（低ノイズアンプ）を検討。

ゲインを調整（高すぎると飽和）。

追跡パラメータの調整:
ini

[Tracking]
pll_bw_hz=40.0  # ノイズ耐性とドップラー追従のバランス
dll_bw_hz=2.0

衛星捕捉失敗:
ログを確認（C/N0値、PRN番号）。

サンプリングレートを8 Mspsに増やす。

設定ファイルのsampling_frequencyが一致しているか確認。

注意点
リアルタイム処理（オプション）：
ini

[GNSS-SDR]
SignalSource.implementation=RTLSDR_Signal_Source
SignalSource.sampling_frequency=4000000

ディスク容量: 長時間キャプチャは大容量（10秒で約1.9 GB）。

ドキュメント: 詳細はGNSS-SDR公式を参照。

