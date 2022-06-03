# Server Scripts

* [**Introduction**](#introduction)
* [**Brand Recognition Inference Server**](#br_infer_server)
* [**Brand Recognition Inference Client**](#br_infer_client)

## <a name="introduction">Introduction

Server scripts are used to power server client architecture. Server scripts are responsible for inference handling and client identification. Server architecture makes it possible to load trained resources automatically for inference, and listens for client for request. Server client architecture communication is based on GRPC.

## <a name="br_infer_server">Brand Recogntion Inference Server

Brand Recognition inference server is responsible of batched inference, results computation and handling of clients. It can track multiple clients and multiple input modes for inference from each client. This [script][ins] take following arguments as input:

```bash
usage: inference_server.py [-h] [-sth SIM_THRES] [-ip SERVER_IP]
                           [-msg MSG_LEN] [-wrk WORKERS] [-emb EMBEDDINGS]

Brand Recognition Inference Server.

optional arguments:
  -h, --help            show this help message and exit
  -sth, --sim_thres     Brand Recognition Similarity Threshold
  -ip, --server_ip      IP Address to Start GRPC Server
  -msg, --msg_len       Message Length Subject to Communication by GRPC
  -wrk, --workers       Number of Workers to Used by GRPC
  -emb, --embeddings    Absolute Address of Embeddings File
```

## <a name="br_infer_client">Brand Recognition Inference Client

Client scripts are used to request images for inference to server. In simple words, they send batch of images to inference server, and return results after process. Usage for this [script][inc] is given as following:

```python
from inference_client import *

brand_recognition_inference_server_ip = '172.17.0.2:1234'

img1 = Image.open('some image path')
img2 = Image.open('some image path')

img_batch = [img1, img2, ...]

target_server = sc_client(brand_recognition_inference_server_ip)

results = target_server(img_batch)

```

[ins]: ./inference_server.py
[inc]: ./inference_client.py