# 嵌入式系統軟體設計與實作

## 內容一覽
- **lab11_pedestrian_detection**：OpenCV 進行行人偵測，HOG+SVM，多尺度與 NMS，繪製人數統計圖。
- **lab12_plate_recognition**：OpenALPR/Tesseract/Leptonica 車牌辨識，處理 6 碼與 7 碼、光線不足等問題。
- **lab13_tvm_rpc**：從原始碼建置 TVM，於樹莓派啟動 RPC，測試 ResNet-18 推論並比較 opt_level 效能與記憶體。

## 專案結構
```
embedded_labs_readmes/
├─ README.md
├─ lab11_pedestrian_detection/
│  └─ README.md
├─ lab12_plate_recognition/
│  └─ README.md
└─ lab13_tvm_rpc/
   └─ README.md
```

## 快速開始
- **行人偵測（Lab 11）**  
  建議先建立 Python venv，安裝 `opencv-python imutils matplotlib` 後，使用 `processing.py`/`video_processing.py` 執行。
- **車牌辨識（Lab 12）**  
  先建置 Leptonica/Tesseract/OpenALPR，或以容器方式準備環境；以 `alpr` 或 `plate_recog.py` 執行。
- **TVM + RPC（Lab 13）**  
  主機建置 TVM、樹莓派建置 runtime 與 RPC server；以 `test.py` 測試不同 `opt_level` 與本地/遠端效能。

## 注意事項
- 樹莓派編譯建議先擴增 swap，降低失敗風險。
- 若相依版本不易處理，建議以 Docker/Podman 容器封裝統一環境。
- 量測與結果請視硬體規格與資料集差異調整。
