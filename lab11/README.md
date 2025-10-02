# 實驗 11｜行人偵測專題（OpenCV + HOG/SVM）

## 簡介
以 OpenCV 取得影像，運用 HOG 特徵配合 SVM 分類器進行行人偵測；延伸以影像金字塔與滑動視窗做多尺度偵測，並繪製每幀偵測人數的統計圖。

## 目標
- 熟悉 OpenCV 影像 I/O 與基本處理。
- 瞭解 HOG 特徵、SVM 分類器與 NMS 的偵測流程。
- 撰寫腳本對影片逐幀統計行人數量，產生圖表。

## 專案結構（建議）
```
lab11_pedestrian_detection/
├─ README.md
├─ env/                # Python 虛擬環境（可選）
├─ processing.py       # 影像/相片偵測
├─ video_processing.py # 影片逐幀偵測
├─ sample.py           # 自行完成之範例
├─ test_opencv.py      # OpenCV 測試
├─ data/
│  ├─ image.jpg        # 測試影像
│  └─ video.mp4        # 測試影片（可自備）
└─ results/
   ├─ frames/          # 輸出逐幀標註影像
   └─ people_count.png # 行人數量統計圖
```

## 需求與安裝
- Python 3.10+（或相容版本）
- OpenCV、imutils、matplotlib

```bash
python -m venv env
source env/bin/activate  # Windows: env\Scripts\activate
pip install opencv-python imutils matplotlib
python test_opencv.py
```

（若需擷取相片）
```bash
sudo apt install fswebcam
fswebcam -r 1280x720 --no-banner ./data/image.jpg
```

## 使用方式
- 單張影像偵測：
```bash
python processing.py --image ./data/image.jpg --out ./results/frames
```

- 影片偵測與人數統計：
```bash
python video_processing.py --video ./data/video.mp4 --save ./results/frames
# 於腳本內累加每幀偵測人數，結束時輸出 results/people_count.png
```

## 方法摘要（HOG/SVM）
1. **梯度計算**：取得每像素水平/垂直梯度與方向。
2. **Cell 分箱**：分割為 cells，依方向直方圖累加梯度強度。
3. **Block 正規化**：鄰近 cells 向量串接並正規化，降低光照影響。
4. **特徵拼接**：全圖（或滑動視窗）之 HOG 向量。
5. **分類與後處理**：以線性 SVM 分類、多尺度金字塔+滑動視窗掃描，最後以 NMS 合併重疊框。

## 常見問題
- **環境缺套件**：請確認 `opencv-python`、`imutils`、`matplotlib` 已安裝且 Python 版本相容。
- **FPS 過低**：可降低輸入影像解析度或調整滑動視窗步長與尺度層數。
- **誤判/漏判**：嘗試調整 SVM 閾值、NMS 參數，或以更適合場景的模型替換（例如 DNN-based detector）。

