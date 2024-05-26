import argparse
import datetime
import json
import numpy as np
import os
import time
from pathlib import Path

import torch
import torch.backends.cudnn as cudnn
from torch.utils.tensorboard import SummaryWriter

import timm

from timm.models.layers import trunc_normal_
from timm.data.mixup import Mixup
from timm.loss import LabelSmoothingCrossEntropy, SoftTargetCrossEntropy

import util.lr_decay as lrd
import util.misc as misc
from util.datasets import build_dataset
from util.pos_embed import interpolate_pos_embed
from util.misc import NativeScalerWithGradNormCount as NativeScaler

import models_vit

from pages.tangwang.model.engine_finetune import train_one_epoch, evaluate, predict_single_image


def predict(image_path, device, nb_classes, input_size):




    probabilities, preclass = predict_single_image(image_path, model, device, num_class=nb_classes, input_size=input_size)
    for class_idx, probability in enumerate(probabilities):
        print(f'Class:{class_idx} Probability:{probability:.4f}')
    print(f'preclass:{preclass}')