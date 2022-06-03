#!/usr/bin/env python3

from inference_client import *
import json
from flask import Flask
from flask import request


# %%
# Execution
app = Flask(__name__)

scbr_server_ip = '0.0.0.0:1235'
scbr_server = br_client(scbr_server_ip)

@app.route('/infer_br_only', methods = ['POST'])
def main_infer():
    json_data = request.json
    
    pil_img_list = list()
    out_dict = dict()
    for i in json_data.values():
        pil_img_list.append(Image.open(i).resize((224, 224)))
    res = scbr_server(pil_img_list)
    for i, j, k in zip(list(json_data.keys()), res[0], res[1]):
        out_dict[i] = {'brand': j, 'matched_filenames': k}

    return out_dict

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8020)