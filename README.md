
# GNSS-SDR Constellation Diagram Generator

このリポジトリは、GNSS-SDRで復調したGPS信号のI/Qデータから、Pythonでコンスタレーション図を表示するツールを提供します。

## 構成
- RTL-SDR + GNSSアンテナで信号キャプチャ
- GNSS-SDRでトラッキング・I/Qデータ出力
- Pythonスクリプトでコンスタレーション図を描画

## 前提条件

### ハードウェア
- RTL-SDR（または互換SDR）
- GPSアンテナ（L1バンド対応）

### ソフトウェア
- Ubuntu 推奨
- GNSS-SDR
- Python 3（依存ライブラリ：`requirements.txt`）

## インストール

```bash
sudo apt-get install rtl-sdr
git clone https://github.com/gnss-sdr/gnss-sdr
cd gnss-sdr && mkdir build && cd build
cmake -DENABLE_GUI=OFF -DENABLE_VOLK=ON ..
make && sudo make install
```
Python環境：
```
pip install -r requirements.txt
```
信号キャプチャ
```
rtl_sdr -f 1575.42e6 -s 4e6 -g 20 -n 40000000 capture/capture.dat
```

GNSS-SDR実行
```
gnss-sdr --config_file=config/front-end-file.conf
```
可視化

オフライン
```
python3 scripts/plot_constellation.py
```
リアルタイム（トラッキング中に表示）
```
python3 scripts/realtime_plot.py
```

参考

GNSS-SDR公式ドキュメント

---
### GNSS-SDR設定
- `front-end-cal.conf`は、GPS L1 C/A信号のオフライン処理用設定ファイルです。
- 主要設定：
  - `SignalSource.filename`: キャプチャファイル（例: `../capture/capture.dat`）を配置。
  - `dump_filename=tracking_PRN_`: PRNごとのI/Qデータ（`tracking_PRN_XX.dat`）を生成。
- 実行：
  ```bash
  gnss-sdr --config_file=front-end-cal.conf
```

