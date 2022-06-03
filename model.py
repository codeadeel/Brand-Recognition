#!/usr/bin/env python3

"""
RESNET-18 MODEL
===============

The following programis the model definition for Brand Recognition
"""

# %%
# Importing Libraries
import os
import pickle
from PIL import Image
import numpy as np
import torch
import torchvision as tv

# %%
# Inference Transforms
inference_transforms = tv.transforms.Compose([
    tv.transforms.Resize((224, 224)),
    tv.transforms.ToTensor(),
    tv.transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# %%
# Input Shape
dummy_input_shape = (1, 3, 224, 224)

# %%
# Main Model Definition
class Model(torch.nn.Module):
    def __init__(self):
        """
        This method is used to initialize model

        Method Input
        ============
        None

        Method Output
        =============
        None
        """
        super(Model, self).__init__()
        self.resnet = tv.models.resnet18(pretrained=True, progress=False)
        self.resnet.requires_grad_(False)
        self.resnet.fc = torch.nn.Flatten()
    
    def forward(self, x):
        """
        This method is used to perform forward propagation on input data

        Method Input
        ============
        x : Input data as image batch ( Batch x Channel x Height x Width )

        Method Output
        =============
        Output results after forward propagation
        """
        return self.resnet(x)
