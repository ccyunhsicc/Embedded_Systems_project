# 行人偵測專題 (Pedestrian Detection Project)

## 專案介紹

本專案是一個關於**嵌入式系統軟體設計與實作**的實驗成果，旨在利用 **OpenCV** 函式庫在 **Raspberry Pi** 上實現基本的**行人偵測系統** 。透過影像處理技術，學習電腦視覺的基礎操作與技巧。

-----

## 實驗目標

  * 學習利用 **OpenCV** 取得影像資訊、進行圖像處理，並最終完成**行人偵測**。
  * 掌握基本的**電腦視覺處理技巧**及**影像基本操作**。
  * 熟悉如何在 **Raspberry Pi** 嵌入式系統上使用 **OpenCV**。
  * **延伸應用**：對影片中的行人進行分析，並使用圖表統計每一幀偵測到的行人數量。

-----

## 環境設置與執行步驟

本實驗主要在 **Raspberry Pi** 上進行操作。

### 1\. 遠端連線與檔案傳輸

| 步驟 | 說明 | 指令 (範例) |
| :--- | :--- | :--- |
| **SSH 連線** | 連線到樹莓派，使用 `-X` 啟用 X11 forwarding，以在本機顯示圖形界面。 | `ssh -X yunhsihsu@172.16.1.53`  |
| **SFTP 傳輸** | 使用 SFTP 將專案檔案傳送到樹莓派上。 | `sftp yunhsihsu@172.16.1.53`  <br> `putr ./pedestrian_detection`  |

### 2\. 環境設置與套件安裝

在樹莓派上設置 Python 虛擬環境並安裝所需套件。

| 步驟 | 說明 | 指令 |
| :--- | :--- | :--- |
| **安裝 Python 3** | 安裝 Python 3。 | `sudo apt install python3`  |
| **創建虛擬環境** | 創建名為 `env` 的虛擬環境。 | `python -m venv env`  |
| **啟用虛擬環境** | 啟用虛擬環境。 | `source env/bin/activate`  |
| **安裝套件** | 安裝 **OpenCV** 和 **imutils** 等必要套件。 | `pip install opencv-python imutils`  |
| **環境測試** | 執行測試程式確認 OpenCV 是否安裝成功。 | `python test_opencv.py`  |

### 3\. 實驗操作與執行

| 步驟 | 檔案 | 說明 | 指令 |
| :--- | :--- | :--- | :--- |
| **圖像處理** | `processing.py` | 觀察並執行單張圖像處理的程式。 | `python processing.py`  |
| **影片處理** | `video_processing.py` | 觀察並執行影片處理程式，進行行人偵測。 | `python video_processing.py`  |
| **拍照測試** | N/A | 安裝 `fswebcam` 並拍照測試。 | `sudo apt install fswebcam`  <br> `fswebcam -r 1280x720 --no-banner ./image.jpg`  |
| **結果產生** | `sample.py` | 完成並執行 `sample.py` 以產生最終結果圖。 | `python sample.py`  |

-----

## 延伸應用：影片中行人數量統計

為了強化對影片與即時影像資料的處理能力，本專案進行了延伸應用：**統計影片中每個時間點出現的行人數量**。

### 實作方式

  * 修改了 `video_processing.py` 程式碼，統計每一幀偵測到的行人出現次數。
  * 使用 Python 的 **matplotlib** 模組進行圖表繪製，視覺化結果。

### 結果圖

下圖展示了影片幀數（Time [s]）與偵測到的行人數量（Number of People）的關係:

圖表顯示，在影片的特定時刻，偵測到的行人數量最高可達 2 位。
