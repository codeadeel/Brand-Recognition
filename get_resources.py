#!/usr/bin/env python3

# %%
# NOTE
# ====
# This file is responsible to download trained resources from Google Drive. Please run this script after cloning this repository to get trained resources.
#
# To install gdown, please visit following repository.
#		https://github.com/wkentaro/gdown

# %%
# Importing Libraries
import os
import gdown

# %%
# Download Configuration

dlinks = {
    'ffmpeg': 'https://drive.google.com/file/d/1mZ-Pst32ZWrLKvFi-pki_kSOFsPVSJOm/view?usp=sharing',
    'youtube-dl' : 'https://drive.google.com/file/d/1y8-9IUxz3s6D9Gw4OjrvhBy7MhRjzOpR/view?usp=sharing',
    'resnet18-f37072fd.pth' : 'https://drive.google.com/file/d/1hAHUpcpekAWKp2IHGA7dUmA14xvN42Mr/view?usp=sharing',
    'Embeddings' : 'https://drive.google.com/file/d/1pvLn0HNLGaTRJhI7mlOs1izSNdMQFV7b/view?usp=sharing' 
}

alternateDlinks = {
    'resnet18-f37072fd.pth' : 'https://drive.google.com/uc?id=1hAHUpcpekAWKp2IHGA7dUmA14xvN42Mr&confirm=t&uuid=421a53a6-b82f-4927-a5cc-ac9eec0a84c9'
}

# %%
# Download Execution

download_addr = '/'.join(__file__.split('/')[:-1]) + '/Resources'

for keys, vals in dlinks.items():
    gdown.download(vals, f'{download_addr}/{keys}', quiet=False, fuzzy=True)
    if not os.path.exists(f'{download_addr}/{keys}'):
        gdown.download(alternateDlinks[keys], f'{download_addr}/{keys}', quiet=False)
        
