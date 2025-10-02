# 實驗 12｜車牌辨識專題（OpenALPR / Tesseract / OpenCV）

## 簡介
以 OpenALPR（結合 OpenCV、Tesseract、Leptonica）建構基礎車牌辨識流程，並撰寫 `plate_recog.py` 與改良版 `plate_recog_more.py`，處理 6 碼與 7 碼車牌與光線不足等情境。

## 目標
- 在樹莓派（或 Linux）上從源碼建置 Tesseract/Leptonica 與 OpenALPR。
- 以命令列或 Python 腳本進行車牌偵測與 OCR。
- 測量執行時間與磁碟空間，並提出可行改良。

## 專案結構（建議）
```
lab12_plate_recognition/
├─ README.md
├─ env/                   # Python 虛擬環境（可選）
├─ plate_recog.py         # 基礎辨識流程
├─ plate_recog_more.py    # 改良：自動位數判斷/規則套用
├─ template/              # 影像處理模板/字典
├─ img/
│  ├─ plate2.jpg          # 測試圖
│  └─ ...                
└─ results/
   └─ *.txt / *.png       # 文字輸出與可視化
```

## 需求與建置摘要
- 需先安裝（或建置）下列元件：`build-essential`、`cmake`、`git`、`libgtk2.0-dev`、`libavcodec-dev`、`libavformat-dev`、`libswscale-dev`、`libatlas-base-dev`、`gfortran` 等。
- 建議建立/啟用 swap（樹莓派常見做法，如 4G swapfile）。
- 從原始碼建置 **Leptonica 1.71**、**Tesseract 3.04.01**，再建置 **OpenALPR**。
- Python 端安裝 `opencv-python`。

> 提示：版本相依性高，請優先確保上述版本或以容器封裝。

## 快速開始
- 命令列辨識：
```bash
cd ./img
alpr plate2.jpg
```

- Python 腳本：
```bash
source ./env/bin/activate
pip install opencv-python
python plate_recog.py      # 讀取 img/*，輸出結果
```

## 已知問題與改良方向
- **6 碼/7 碼混用**：原程式將 `num_of_digits=7` 寫死，造成舊式 6 碼車牌失敗。→ 以 `plate_recog_more.py` 自動判位數，並套用 7 碼車牌規則，減少英數位置誤判。
- **光線不足**：相機/照片曝光不足導致可讀性差。→ 增加自動亮度/對比增強（CLAHE）、去噪、形態學處理。
- **誤檢與誤讀**：依國內車牌格式過濾不合規結果，再以字典修正常見混淆（O/0、I/1、B/8…）。

## 度量（建議）
- **時間**：以 `time.time()` 或 `timeit` 記錄影像處理與 OCR 時間。
- **空間**：以 `du -sh env/ plate_recog.py template/ img/` 粗估模組/資料大小。

## 故障排除
- **OpenALPR 無法執行**：確認 `ldconfig` 已更新、動態連結路徑正確。
- **Tesseract 找不到語言包**：安裝/指定正確 `tessdata` 位置與語言。
- **CPU/記憶體不足**：降低影像尺寸、啟用 swap、關閉不必要服務。
