#!/usr/bin/env python3

"""
BRAND RECOGNITION INFERENCE
===========================

The following program is used to perform inference on the subject data
"""

# %%
# Importing Libraries
from socket import socket
from model import *
import time
import sys
import argparse
import socket
from concurrent import futures
import grpc
import communication_pb2
import communication_pb2_grpc

# %%
# Main Inference Class
class Inference:
    def __init__(self, embed, conf_thres=0.7):
        """
        This method is used to initialize model inference

        Method Input
        ============
        embed : Absolute address of embeddings file
        conf_thres : Brand Recognition similarity threshold

        Method Output
        =============
        None
        """
        torch.cuda.empty_cache()
        self.embedding_data_address = embed
        self.__conf_thres__ = conf_thres
        self.__device__ = 'cuda:0' if torch.cuda.is_available() else 'cpu'
        self.mod = Model()
        self.mod.to(self.__device__)
        self.mod.eval()
        print('>>>>> Inference Model Loaded')
        with open(self.embedding_data_address, 'rb') as efile1:
            self.embeddings = pickle.load(efile1)
            self.__brand_list__ = list(set(self.embeddings['tags']))
        self.__emb_tensors = torch.Tensor(self.embeddings['embeds']).to(self.__device__)
        self.__emb_tags = self.embeddings['tags']
        self.__emb_addr = self.embeddings['addrs']
        del self.embeddings
        print('>>>>> Brand Recognition Labels Loaded')
        self.__cos = torch.nn.CosineSimilarity(dim=2, eps=1e-6)

    def __str__(self):
        """
        This method is __str__ implementation of subject class

        Method Input
        ============
        None

        Method Output
        =============
        New Line
        """
        print(f'Acceleration Device: {self.__device__}')
        print(f'Brand Recognition Similarity Threshold: {self.__conf_thres__}')
        print(f'Number of Brand Recognition Labels: {len(self.__brand_list__)}')
        print(f'Brand Recognition Labels: {self.__brand_list__}')
        return '\n'
    
    def __input_batch__(self, btch_dat):
        """
        This method converts stacked Numpy PIL images to stacked Torch tensors

        Method Input
        ============
        btch_dat : Stacked Numpy PIL images with following dimensions:
                            [ Batch x Width x Height x Channel ]

        Method Output
        =============
        Torch Tensor
        """
        input_tensors = [inference_transforms(Image.fromarray(i)) for i in btch_dat]
        return torch.stack(input_tensors)

    def __feature_matching__(self, inf_embeds):
        """
        This method is used to find cosine similarity on GPU

        Method Input
        ============
        inf_embeds : Brand Recognition embeddings output in the form of Torch tensors

        Method Output
        =============
        Tuple of similarity score & respective index as Numpy array
                            ( Similarity Score, Respective Index )
        """
        res = self.__cos(inf_embeds.unsqueeze(1), self.__emb_tensors)
        sorter, indx = torch.sort(res)
        return [sorter.cpu().detach().numpy()[:, -1], indx.cpu().detach().numpy()[:, -1]]
    
    def __call__(self, img_btch, cliend_id='abcdefghij'):
        """
        This method is used to perform Brand Recognition inference

        Method Input
        ============
        img_btch : Stackd Numpy PIL images with following shape:
                            [ Batch x Width x Height x Channel ]
        """
        img_btch = self.__input_batch__(img_btch)
        inf1 = self.mod(img_btch.to(self.__device__))
        br_embeds = self.__feature_matching__(inf1)
        lister, addr_lister = list(), list()
        for i in br_embeds[1]:
            if i>=0:
                lister.append(self.__emb_tags[i])
                addr_lister.append(self.__emb_addr[i])
            else:
                lister.append('Unknown')
                addr_lister.append('Unknown')
        return lister, inf1.cpu().detach().numpy(), addr_lister

# %%
# Inference Server Class
class br(communication_pb2_grpc.brServicer):
    def __init__(self, *args, **kwargs):
        """
        This method is used to initialize server class for model inference

        Method Input
        ============
        None

        Method Output
        =============
        None
        """
        pass

    def _request_processor(self, inp_req):
        """
        This method is used to process input request to server

        Method Input
        ============
        inp_req : Request object generated by GRPS

        Method Output
        =============
        Input data for inference as Numpy array along with client id
                            ( Input Numpy Data, Client ID )
        """
        ret_dat = np.frombuffer(inp_req.imgs, dtype=inp_req.data_type).reshape(inp_req.batch, inp_req.width, inp_req.height, inp_req.channel)
        print(f'Input Batch Shape: {ret_dat.shape}')
        return ret_dat, inp_req.client_id
    
    def _output_processor(self, inf_out):
        """
        This method is used to process output data after inference

        Method Input
        ============
        inf_out : Brand Recognition inference as tuple
                            ( Brand Recognition Inference List )
        
        Method Output
        =============
        Output object after inference
        """
        return communication_pb2.server_output(
            brand_recognition = np.array(inf_out[0]).tobytes(),
            brand_labels_filenames = np.array(inf_out[2]).tobytes(),
            embeddings = inf_out[1].tobytes(),
            height = inf_out[1].shape[0],
            width = inf_out[1].shape[1],
            data_type = inf_out[1].dtype.name
        )
    
    def inference(self, request, context):
        """
        This method is used to handle requests & inference outputs

        Method Input
        ============
        request : GRPC generated input request object
        context : GRPC generated API context

        Method Output
        =============
        None
        """
        inp_data, client_id = self._request_processor(request)
        print(f'Client ID: {client_id}')
        st = time.time()
        out_data = inf_obj(inp_data, client_id)
        ed = time.time() - st
        print(f'Inference Time: {ed}')
        print(f'Brand Recognition: {out_data[0]}')
        print(f'Brand Recognition Respective Filenames: {out_data[2]}')
        print(f'Embedding Size: {out_data[1].shape}')
        print('---------------------------------------------\n')
        return self._output_processor(out_data)

# %%
# Server Execution
if __name__=='__main__':
    parser = argparse.ArgumentParser(description = 'Brand Recognition Inference Server.')
    parser.add_argument('-sth', '--sim_thres', type = float, help = 'Brand Recognition Similarity Threshold', default = 0.7)
    parser.add_argument('-ip', '--server_ip', type = str, help = 'IP Address to Start GRPC Server', default = '[::]:1235')
    parser.add_argument('-msg', '--msg_len', type = int, help = 'Message Length Subject to Communication by GRPC', default = 1000000000)
    parser.add_argument('-wrk', '--workers', type = int, help = 'Number of Workers to Used by GRPC', default = 1)
    parser.add_argument('-emb', '--embeddings', type = str, help = 'Absolute Address of Embeddings File', default = '/resources/Embeddings')
    args = vars(parser.parse_args())
    print("""
    ======================================
    | Brand Recognition Inference Server |
    ======================================
    """)
    inf_obj = Inference(embed = args['embeddings'], conf_thres = args['sim_thres'])
    print('---------------------------------------------')
    print(inf_obj)
    print("""
    =============================================
    |       Inference GRPC Server Details       |
    =============================================
    """)
    duip, msle, wrke = args['server_ip'], args['msg_len'], args['workers']
    print(f'Inference IP: {duip}')
    print(f'Server IP: {socket.gethostbyname(socket.gethostname())}')
    print(f'Maximum Server Communication Message Length: {msle}')
    print(f'Number of Worker Allowed for GRPC Server: {wrke}')
    print('---------------------------------------------')
    print('>>>>> Press Ctrl+C To Shutdown Server')
    print("""
    =============================================
    |              Inference Logs               |
    =============================================
    """)
    server_opts = [('grpc.max_send_message_length', args['msg_len']), ('grpc.max_receive_message_length', args['msg_len'])]
    server = grpc.server(futures.ThreadPoolExecutor(max_workers = args['workers']), options = server_opts)
    communication_pb2_grpc.add_brServicer_to_server(br(), server)
    server.add_insecure_port(args['server_ip'])
    server.start()
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("""
    =============================================
    |               Shutting Down               |
    =============================================
    """)
        sys.exit(0)
