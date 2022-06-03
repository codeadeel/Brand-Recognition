# Brand Recognition

* [**Introduction**](#introduction)
* [**Architecture**](#architecture)
* [**Repository Cloning**](#cloner)
* [**Container Build**](#container_build)
  * [**Brand Recognition Inference Server**](#br_infer_server)
  * [**Client: *Embedding Generator Client***](#emb_gen_client)
  * [**Client: *Live Stream Local Display***](#live_stream_local)
  * [**Client: *Live Stream Browser***](#live_stream_browser)
  * [**Client: *Live Stream RTSP***](#live_stream_rtsp)
  * [**Client: *Multi Live Stream Browser***](#multi_live_stream_browser)
  * [**Client: *Multi Live Stream RTSP***](#multi_live_stream_rtsp)
  * [**Client: *Local Stream Local Display***](#local_stream_local)
  * [**Client: *Local Stream Browser***](#local_stream_browser)
  * [**Client: *Local Stream RTSP***](#local_stream_rtsp)
  
## <a name="introduction">Introduction

The subject code is responsible for Brand Recognition. Final classification is implemented as server-client architecture. Scenes under consideration are segregated using features extraction and matching using deep learning tools. This system can be applied on multiple streams for identification of different scenes, already available in feature store. Simply explained, if a scene to be tracked is available, it can be identified on live stream.

The model used in this architecture is ***ResNet-18***, on ***Pytorch*** framework.

## <a name="architexture">Architecture

The whole system is based on server-client architecture. This allows easy usablity and integration without multi accelaration devices and extra resource consumption. The macro architecture is shown below:

![Brand Recognition Macro Architecture][macro_architecture]

The above macro architecture is based on following pointers:

* Everything is containerized.
* Embeddings can be generated using a client and request generator to server using GRPC.
* Generated embeddings with respective frames can be exported to persistent storage, later accessed by server.
* Output resources will be loaded by **Brand Recognition Inference Server**, and server will be ready for inference.
* Multiple clients can connect to a single server for inference in ***batched mode***, using GRPC.

The micro architecture is also shown below:

![Brand Recognition Micro Architecture][micro_architecture]

The above micro architecture is based on follwoing pointer:

* Everything is containerized.
* Input images will be converted to batches using batch handler.
* Batched of images will be sent to AI inference server using request handler.
* AI inference server handles batched inputs using GRPC with client identification.
* Input batch will be processed to CUDA tensor.
* Inference will be done on ***GPU / CPU*** in Pytorch.
* Results are returned to respective client using request handler.
* Request handler on the client side, processes results and make it ready for utilization.

## <a name="cloner">Repository Cloning

The prerequisite for this repository is [***gdown***][gdown_link] library. It is required to download trained resources from Google Drive. The cloning and setup procedure for this repository is given below:

```bash
# To clone repository after setting up gdown
git clone https://github.com/codeadeel/Brand-Recognition.git

# To download trained resources
cd ./Brand-Recognition
chmod 777 ./get_resources.py
./get_resources.py
```

## <a name="container_build">Container Build

Every component of architecture is containerized, so container building container and respective execution requires certain set of commands. Following commands can be used for respective container builds:

### <a name="br_infer_server">Brand Recognition Inference Server

Brand Recognition inference server is responsible of batched inference, results computation and handling of clients. It can track multiple clients and multiple input modes for inference from each client. To build the container, following command can be used:

```bash
docker build -t brand_recognition:server -f Build_Server .
```

Also, to execute container, following command can be used:

```bash
docker run --rm -it --gpus all \
    -v [ Optional: Your Path to Embeddings File ]:/resources/Embeddings \
    -p [ Your Port to Expose Server ]:1235 \
    brand_recognition:server [ Your Arguments ]
```

### <a name="emb_gen_client">Client: ***Embedding Generator Client***

This client is used to generate embeddings for the scenes, by performing inference through server. If no embeddings are already available, then new feature store will be created else, existing embeddings will be updated. To build the container, following command can be used:

```bash
docker build -t brand_recognition:embeddings -f Embeddings_Client .
```

Also, to execute container, following command can be used:

```bash
docker run --rm -it
    -v [ Required: Your Path to Video File ]:/video.mp4 \
    -v [ Required: Your Directory Path to Save Generated / Updated Embeddings ]:/Output \
    -v [ Required / Optional : Your Path to Existing Binary Embedding File in Case of Update ]:/Embeddings:ro \
    brand_recognition:embeddings [ Your Arguments ]
```

### <a name="live_stream_local">Client: ***Live Stream Local Display***

This client can be used to perform inference on live stream, and display results on local display, using .X11 socket. To build the container, following command can be used:

```bash
docker build -t brand_recognition:live_client -f Live_Client .
```

Also, to execute container, following command can be used:

```bash
docker run --rm -it \
    -v [ Optional: Your Directory Path to Save Output ]:/Output \
    brand_recognition:live_client [ Your Arguments ]
```

### <a name="live_stream_browser">Client: ***Live Stream Browser***

This client can be used to perform inference on live stream, and display results through webpage. To build the container, following command can be used:

```bash
docker build -t brand_recognition:live_client_browser -f Live_Client_Browser .
```

Also, to execute container, following command can be used:

```bash
docker run --rm -it \
    -v [ Optional: Your Directory Path to Save Output ]:/Output \
    -p [ Optional: Your Port to Expose ]:80 \
    brand_recognition:live_client_browser [ Your Arguments ]
```

### <a name="live_stream_rtsp">Client: ***Live Stream RTSP***

This client can be used to perform inference on live stream, and display results through RTSP stream. To build the container, following command can be used:

```bash
docker build -t brand_recognition:live_client_rtsp -f Live_Client_RTSP .
```

Also, to execute container, following command can be used:

```bash
docker run --rm -it \
    -v [ Optional: Your Directory Path to Save Output ]:/Output \
    -p [ Optional: Your Port to Expose ]:80 \
    brand_recognition:live_client_rtsp [ Your Arguments ]
```

### <a name="multi_live_stream_browser">Client: ***Multi Live Stream Browser***

This client can be used to perform inference on multiple live streams, and display results on through webpage. To build the container, following command can be used:

```bash
docker build -t brand_recognition:multi_live_browser -f Multi_Live_Client_Browser .
```

Also, to execute container, following command can be used:

```bash
docker run --rm -it \
    -p [ Optional: Your Port to Expose ]:80 \
    brand_recognition:multi_live_client_browser [ Your Arguments ]
```

### <a name="multi_live_stream_rtsp">Client: ***Multi Live Stream RTSP***

This client can be used to perform inference on multiple live streams, and display results through RTSP stream. To build the container, following command can be used:

```bash
docker build -t brand_recognition:multi_live_rtsp -f Multi_Live_Client_RTSP .
```

Also, to execute container, following command can be used:

```bash
docker run --rm -it \
    -p [ Optional: Your Port to Expose ]:80 \
    brand_recognition:multi_live_client_rtsp [ Your Arguments ]
```

### <a name="local_stream_local">Client: ***Local Stream Local Display***

This client can be used to perform inference on local video, and display results on local display, using .X11 socker. To build constainer, following command can be used:

```bash
docker build -t brand_recognition:video_client -f Video_Client .
```

Also, to execute container, following command can be used:

```bash
docker run --rm -it \
    -v [ Required: Your Path to Video File]:/video.mp4 \
    -v [ Optional: Your Directory Path to Save Output ]:/Output \
    brand_recognition:video_client [ Your Arguments ]
```

### <a name="local_stream_browser">Client: ***Local Stream Browser***

This client can be used to perform inference on local stream, and display results through webpage. To build the container, following command can be used:

```bash
docker build -t brand_recognition:video_client_browser -f Video_Client_Browser .
```

Also, to execute container, following command can be used:

```bash
docker run --rm -it \
    -v [ Required: Your Path to Video File]:/video.mp4 \
    -v [ Optional: Your Directory Path to Save Output ]:/Output \
    -p [ Optional: Your Port to Expose ]:80 \
    brand_recognition:video_client_browser [ Your Arguments ]
```

### <a name="local_stream_rtsp">Client: ***Local Stream RTSP***

This client can be used to perform inference on local stream, and display results through RTSP stream. To build the container, following command can be used:

```bash
docker build -t brand_recognition:video_client_rtsp -f Video_Client_RTSP .
```

Also, to execute container, following command can be used:

```bash
docker run --rm -it \
    -v [ Required: Your Path to Video File]:/video.mp4 \
    -v [ Optional: Your Directory Path to Save Output ]:/Output \
    -p [ Optional: Your Port to Expose ]:80 \
    brand_recognition:video_client_rtsp [ Your Arguments ]
```


[macro_architecture]: ./MarkDown-Data/macro_architecture.jpg
[micro_architecture]: ./MarkDown-Data/micro_architecture.jpg
[gdown_link]: https://github.com/wkentaro/gdown