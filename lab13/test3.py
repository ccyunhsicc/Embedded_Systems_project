import numpy as np
import tvm
from tvm import te,relay,rpc
from tvm.contrib import utils,graph_executor
import tvm.relay.testing
from tvm.contrib.download import download_testdata
from torchvision.models import resnet18,ResNet18_Weights
from PIL import Image
import time
import os
import psutil

def get_cat_image():
    url="https://gist.githubusercontent.com/zhreshold/bcda4716699ac97ea44f791c24310193/raw/fa7ef0e9c9a5daea686d6473a62aacd1a5885849/cat.png"
    dst="cat.png"
    real_dst=download_testdata(url,dst,module="data")
    img=Image.open(real_dst).resize((224,224))
    # Preprocess the image using PyTorch's ResNet-18 weights
    weights=ResNet18_Weights.DEFAULT
    preprocess=weights.transforms()
    img_tensor=preprocess(img).unsqueeze(0) #(3, 224, 224) -> (1, 3, 224, 224)
    # Convert to numpy array with the correct data type
    img_array=img_tensor.numpy()
    return np.asarray(img_array,dtype="float32")
#---------------------------------------
batch_size=1
num_class=1000
image_shape=(3,224,224)
data_shape=(batch_size,)+image_shape
#
# get_workload: Retrieves a pre-defined ResNet-18 model in Relay's intermediate
#               representation, along with its parameters.
# mod: Represents the computational graph of the model.
# params: Contains the model's parameters, such as weights and biases.
#
mod,params=relay.testing.resnet.get_workload(num_layers=18,batch_size=batch_size,image_shape=image_shape)
#---------------------------------------
# Compilation configuration.
#
local_demo=False
if local_demo:
    target="llvm"
else:
    # target ARM-based devices, such as Raspberry Pi.
    target="llvm -mtriple=aarch64-linux-gnu"

#---------------------------------------
# Establish RPC connection.
#
if local_demo:
    remote=rpc.LocalSession()
else:
    # The following is my environment, change this to the IP address of your target device
    host="172.16.1.53"
    port=9090
    remote=rpc.connect(host,port)

for i in range(4):
    if i==1 or i==2:
        continue
    #---------------------------------------
    # Compile the model using TVM.
    #
    print(f"opt-level = {i}")
    with tvm.transform.PassContext(opt_level=i):
        #build_start=time.time()
        build_rss_start = psutil.Process().memory_info().rss / (1024 * 1024)
        lib=relay.build(mod,target,params=params)
        #build_end=time.time()
        build_rss_end = psutil.Process().memory_info().rss / (1024 * 1024)
        #print(f"build time = {build_end-build_start}")
    
    print(f"Build memory usage: {build_rss_end-build_rss_start:.2f} MB")
    #
    # save the compiled library at a local temp folder.
    #
    temp=utils.tempdir()
    path=temp.relpath(f"lib{i}.tar")
    lib.export_library(path)
    
    # upload the library to the remote device.
    remote.upload(path)
    # Load the library on the remote device, making it ready for execution.
    rlib=remote.load_module(f"lib{i}.tar")
    #---------------------------------------
    # Execute the model.
    #
    # Specifie the CPU device on the remote machine.
    dev=remote.cpu(0)
    # Wrap the loaded module for execution.
    module=graph_executor.GraphModule(rlib["default"](dev))
    # Set input data and parameters.
    module.set_input("data",get_cat_image(),**params)
    # Execute the model.
    #run_start=time.time()
    run_rss_start = psutil.Process().memory_info().rss / (1024 * 1024)
    module.run()
    #run_end=time.time()
    run_rss_end = psutil.Process().memory_info().rss / (1024 * 1024)
    print(f"Run memory usage: {run_rss_end-run_rss_start:.2f} MB")
    #print(f"run time = {run_end-run_start}")
    # Get output
    out=module.get_output(0).numpy()
    #print("output",out)
