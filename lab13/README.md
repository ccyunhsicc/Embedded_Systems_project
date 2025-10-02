# 實驗 13｜從原始碼建置 TVM，並以 RPC 在樹莓派部署推論

## 簡介
於主機自建 TVM（v0.18），在樹莓派端編譯 TVM Runtime 與啟動 RPC 伺服器；本機透過 RPC 在樹莓派執行 ResNet-18 推論，並比較不同 `opt_level`（0,1,2,3）對 **編譯時間**、**執行時間**、**記憶體** 的影響，同時比較本地與遠端的效能差異。

## 專案結構（建議）
```
lab13_tvm_rpc/
├─ README.md
├─ lab13/                 # Python venv（主機端）
├─ env/                   # Python venv（樹莓派端）
├─ tvm/                   # 來源樹（主機/樹莓派各一份）
├─ test.py                # 測試/量測腳本（含 opt_level 與 psutil 量測）
└─ results/
   └─ *.json / *.csv      # 量測結果輸出
```

## 建置摘要

### 主機端（Build TVM）
```bash
sudo apt-get install -y python3 python3-dev python3-setuptools \
  gcc git libtinfo-dev zlib1g-dev build-essential cmake libedit-dev \
  libxml2-dev llvm-dev llvm ninja-build

wget https://dlcdn.apache.org/tvm/tvm-v0.18.0/apache-tvm-src-v0.18.0.tar.gz
tar zxvf apache-tvm-src-v0.18.0.tar.gz && mv apache-tvm-src-*/ tvm
cd tvm && mkdir -p build && cd build && cp ../cmake/config.cmake .

cat >> config.cmake <<'EOF'
set(USE_LLVM ON)
set(HIDE_PRIVATE_SYMBOLS ON)
set(USE_CUDA OFF)
set(USE_METAL OFF)
set(USE_VULKAN OFF)
set(USE_OPENCL OFF)
set(USE_CUBLAS OFF)
set(USE_CUDNN OFF)
set(USE_CUTLASS OFF)
set(USE_GRAPH_EXECUTOR ON)
set(USE_PROFILER ON)
set(CMAKE_BUILD_TYPE Release)
EOF

cmake .. -G Ninja
ninja

echo 'export TVM_HOME=~/tvm' >> ~/.bashrc
echo 'export PYTHONPATH=$TVM_HOME/python:$PYTHONPATH' >> ~/.bashrc
source ~/.bashrc

python3 -m venv ./lab13 && source ./lab13/bin/activate
pip install numpy decorator attrs typing-extensions psutil scipy packaging Pillow torchvision tornado
python -c "import tvm; print(tvm.__version__)"
```

### 樹莓派端（Build Runtime + RPC）
```bash
ssh -X <user>@<rpi-ip>

wget https://dlcdn.apache.org/tvm/tvm-v0.18.0/apache-tvm-src-v0.18.0.tar.gz
tar zxvf apache-tvm-src-v0.18.0.tar.gz && mv apache-tvm-src-*/ tvm
cd tvm && mkdir -p build && cd build && cp ../cmake/config.cmake .

# 建議先擴增 swap，避免編譯中途失敗
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

echo 'set(USE_GRAPH_EXECUTOR ON)' >> config.cmake
cmake .. -G Ninja
ninja runtime -v -j3

echo 'export TVM_HOME=~/tvm' >> ~/.bashrc
echo 'export PYTHONPATH=$TVM_HOME/python:$PYTHONPATH' >> ~/.bashrc
source ~/.bashrc

python3 -m venv ./env && source ./env/bin/activate
pip install numpy decorator attrs typing-extensions psutil tornado packaging torchvision cloudpickle

# 啟動 RPC Server
python -m tvm.exec.rpc_server --host 0.0.0.0 --port=9090
```

## 測試與量測
- 於主機端執行：
```bash
pip install pytest
python test.py
```

- `test.py` 建議內容：
  - 以 `relay.build(mod, target, params)` 量測 **build time**。
  - 以 `module.run()` 量測 **run time**。
  - 以 `psutil` 於 **build** 與 **run** 階段記錄記憶體峰值。
  - 切換 `opt_level = {0,1,2,3}` 比較：
    - 0：無優化（基本型別/形狀檢查）。
    - 1：常數折疊、死程式碼刪除。
    - 2：算子融合、資料布局轉換。
    - 3：向量化、迴圈展開、SIMD、排程與預取。
  - 切換 `local_demo=True/False` 比較本地與遠端效能。

## 常見問題
- **樹莓派卡頓/當機**：務必啟用 4G 以上 swap、降低 `-j` 併行度。
- **匯入 TVM 失敗**：確認 `PYTHONPATH` 指向 `tvm/python`。
- **RPC 無法連線**：檢查 RPi 防火牆、9090 埠、同網段可達性。
