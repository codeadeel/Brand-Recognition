#!/usr/bin/env python3

"""
BRAND RECOGNITION INFERENCE CLIENT
==================================
The following program is used to perform inference on the subject data
"""

# %%
# Importing Libraries
from PIL import Image
import numpy as np
import grpc
import communication_pb2
import communication_pb2_grpc

# %%
# Main Client Inference Class
class br_client:
    def __init__(self, server_ip, id_len = 10):
        """
        This method is used to initialize Brand Recognition inference client

        Method Input
        =============
        server_ip : Server IP at which GRPC server is running
                            Format : "IP:Port"
                            Example : '0.0.0.0:1235'
        id_len : Length of client randomized id ( default : 10 )

        Method Output
        ==============
        None
        """
        self.br_server_ip = server_ip
        self.channel = grpc.insecure_channel(self.br_server_ip)
        self.stub = communication_pb2_grpc.brStub(self.channel)
        self.client_name_chars = np.array(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'])
        self.client_name = ''.join(np.random.choice(self.client_name_chars, size = id_len).tolist())
    
    def input_processor(self, inp1):
        """
        This method is used to process input & sends request to GRPC server

        Method Input
        =============
        inp1 : Input for inference request as Numpy array
                            [ Batch x Width x Height x Channel ]

        Method Output
        ==============
        Request to GRPC server
        """
        inp1_shape = inp1.shape
        self.__batch_size = inp1_shape[0]
        return communication_pb2.server_input(imgs = inp1.tobytes(), batch = inp1_shape[0], width = inp1_shape[1], height = inp1_shape[2], channel = inp1_shape[3], data_type = inp1.dtype.name, client_id = self.client_name)
    
    def output_processor(self, out1):
        """
        This method is used to process output by receiving response from GRPC server

        Method Input
        =============
        out1 : GRPC server response after inference

        Method Output
        ==============
        Response from GRPC server
        """
        br_recog = [''.join(i) for i in np.frombuffer(out1.brand_recognition, dtype = '<U1').reshape(self.__batch_size, -1)]
        br_addrs = [''.join(i) for i in np.frombuffer(out1.brand_labels_filenames, dtype = '<U1').reshape(self.__batch_size, -1)]
        embeddings = np.frombuffer(out1.embeddings, dtype = out1.data_type).reshape(out1.height, out1.width)
        return br_recog, br_addrs, embeddings

    def __call__(self, x):
        """
        This method is used to handle inference requests & returns inference results

        Method Input
        =============
        x : List of Pillow images subject to required inference

        Method Output
        ==============
        Brand Recognition inference as tuple
                             ( Brand Recognition Inference List, Brand Recognition Address List, Embeddings Against Frames )
        """
        x = np.stack([np.asarray(i) for i in x])
        response = self.stub.inference(self.input_processor(x))
        return self.output_processor(response)
    
    def __del__(self):
        """
        This method is used to close communication channel to GRPC server
        
        Method Input
        =============
        None
        
        Method Output
        ==============
        None
        """
        self.channel.close()
