#!/usr/bin/env python3

"""
BRAND RECOGNITION EMBEDDINGS GENERATION CLIENT
==============================================

The following program is used to update embeddings files and frames
"""

# %%
# Importing Libraries
from inference_client import *
import os
import argparse
import json
import pickle
import tqdm
import cv2 as ocv

# %%
# Main Embeddings Extraction Class
class Embeddings:
    def __init__(self, addr, server_ip, emb_label, embed, sv_embed):
        """
        This method is used to initialize Brand Recognition embedding generation client

        Method Input
        =============
        addr : Local address to data
        server_ip : Server IP at which GRPC server is running
                            Format : "IP:Port"
                            Example : '0.0.0.0:1235'
        emb_label : Label for the current generated embeddings
        embed : Absolute address of the embeddings file
        sv_embed : Absolute address of directory to save embedding in binary & JSON

        Method Output
        ==============
        None
        """
        self.vid_addr = addr
        self.embedding_label = emb_label
        self.embedding_data_address = embed
        self.embedding_save_directory = sv_embed
        self.scbr_server_ip = server_ip
        self.scbr_inference = br_client(self.scbr_server_ip)
        self.__vid_obj__ = ocv.VideoCapture(self.vid_addr)
        self.FPS = int(self.__vid_obj__.get(ocv.CAP_PROP_FPS))
        self.height = int(self.__vid_obj__.get(ocv.CAP_PROP_FRAME_HEIGHT))
        self.width = int(self.__vid_obj__.get(ocv.CAP_PROP_FRAME_WIDTH))
        self.__total_frames__ = int(self.__vid_obj__.get(ocv.CAP_PROP_FRAME_COUNT))
        self.__new_embeddings__ = dict()
        try:
            with open(self.embedding_data_address, 'rb') as efile1:
                self.embeddings = pickle.load(efile1)
            self.__embeddings_available__ = True
            self.__new_embeddings__['embeds'] = np.array(self.embeddings['embeds'])
            self.__new_embeddings__['tags'] = self.embeddings['tags']
            self.__new_embeddings__['addrs'] = self.embeddings['addrs']
            self.__brand_list__ = list(set(self.__new_embeddings__['tags']))
        except:
            self.__embeddings_available__ = False
            self.__brand_list__ = list()
        if not os.path.exists(f'{self.embedding_save_directory}/Frames'):
            os.mkdir(f'{self.embedding_save_directory}/Frames')
    
    def __str__(self):
        """
        This method is __str__ implementation of subject class

        Method Input
        =============
        None
        
        Method Output
        ==============
        New Line
        """
        print("""
        ==================================================
        | Brand Recognition Embeddings Generation Client |
        ==================================================
        """)
        print(f'Current Embedding Label: {self.embedding_label}')
        print(f'Brand Recognition Server IP Address: {self.scbr_server_ip}')
        print(f'Client ID: {self.scbr_inference.client_name}')
        print(f'Video FPS: {self.FPS}')
        print(f'Video Height: {self.height}')
        print(f'Video Width: {self.width}')
        print(f'Total Video Frames: {self.__total_frames__}')
        print(f'Number of Brand Recognition Labels: {len(self.__brand_list__)}')
        print(f'Brand Recognition Labels: {self.__brand_list__}')
        print(f'Embeddings Extraction Address: {self.embedding_save_directory}')
        print('\n---------------------------------------------')
        return '\n'
    
    def __embedding_handler__(self, data, labels, new_addrs):
        """
        This method is used to save & handle embeddings

        Method Input
        =============
        data : New generated embeddings data
        labels : New labels for the respective generated embeddings
        new_addrs : New embeddings frames addresses

        Method Output
        ==============
        None
        """
        print('>>>>> Processing Embeddings')
        if self.__embeddings_available__ == True:
            self.__new_embeddings__['embeds'] = np.append(self.__new_embeddings__['embeds'], np.array(data), axis = 0)
            self.__new_embeddings__['tags'].extend(labels)
            self.__new_embeddings__['addrs'].extend(new_addrs)
        else:
            self.__new_embeddings__['embeds'] = np.array(data)
            self.__new_embeddings__['tags'] = labels
            self.__new_embeddings__['addrs'] = new_addrs
        print('>>>>> Saving Embeddings as Binary')
        with open(f'{self.embedding_save_directory}/Embeddings', 'wb') as file1:
            pickle.dump(self.__new_embeddings__, file1)
        print('>>>>> Saving Embeddings as JSON')
        with open(f'{self.embedding_save_directory}/Embeddings.json', 'w') as file1:
            self.__new_embeddings__['embeds'] = self.__new_embeddings__['embeds'].tolist()
            json.dump(self.__new_embeddings__, file1)
    
    def __call__(self, skip = 0):
        """
        This method is used to generate embeddings from subject video file

        Method Input
        =============
        skip : Number of frames to skip in local video inference ( default : 0 )

        Method Output
        ==============
        None
        """
        new_emb_labels, new_embs, new_addrs = list(), list(), list()
        count, skip_count, ret = 0, skip, True
        with tqdm.tqdm(total = self.__total_frames__, bar_format = '{l_bar}{bar:10}{r_bar}{bar:-10b}', position = 0, leave = True) as bar:
            while ret:
                ret, cv_dat = self.__vid_obj__.read()
                if not ret:
                    break
                if skip_count < skip:
                    skip_count += 1
                else:
                    skip_count = 0
                    pil_dat = Image.fromarray(ocv.cvtColor(cv_dat, ocv.COLOR_BGR2RGB))
                    res = self.scbr_inference([pil_dat])
                    new_emb_labels.append(self.embedding_label)
                    new_embs.append(res[2][0])
                    ocv.imwrite(f'{self.embedding_save_directory}/Frames/{self.embedding_label}_' + str(count).zfill(10) + '.jpg', cv_dat)
                    new_addrs.append(f'{self.embedding_label}_' + str(count).zfill(10) + '.jpg')
                count += 1
                bar.set_description(f'Label: {self.embedding_label} | Skipping {skip} Frames | Progress') 
                bar.update(1)
        self.__embedding_handler__(new_embs, new_emb_labels, new_addrs)
        os.system(f'chmod 777 /{self.embedding_save_directory}/*')
        os.system(f'chmod 777 /{self.embedding_save_directory}/Frames/*')

# %%
# Embeddings Generation Execution
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Brand Recognition Embedding Generation Client.')
    parser.add_argument('-ip', '--server_ip', type = str, help = 'IP Address to GRPC Server => IP:Port', required = True)
    parser.add_argument('-lab', '--label', type = str, help = 'Label Against Subject Video for Embeddings Generation', required = True)
    parser.add_argument('-sk', '--skip', type = int, help = 'Number of Frames to Skip in Embeddings Generation', default = 0)
    parser.add_argument('-l', '--link', type = str, help = 'Local Video Address', default = '/video.mp4' )
    parser.add_argument('-embl', '--embedding_addr', type = str, help = 'Current Available Embeddings File', default = '/Embeddings' )
    parser.add_argument('-embs', '--embedding_save', type = str, help = 'Directory to Save Embeddings Files', default = '/Output' )
    args = vars(parser.parse_args())
    emb = Embeddings(addr = args['link'], server_ip = args['server_ip'], emb_label = args['label'], embed = args['embedding_addr'], sv_embed = args['embedding_save'])
    print(emb)
    emb(skip = args['skip'])
    