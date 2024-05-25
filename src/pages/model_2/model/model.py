import torch
import models_vit
from .util.pos_embed import interpolate_pos_embed
from timm.models import trunc_normal_

import config as cfg

class TangwangModel:
    def __init__(self):
        # call the model
        self.model = models_vit.__dict__['vit_large_patch16'](
            num_classes=2,
            drop_path_rate=0.2,
            global_pool=True,
        )

        self.checkpoint = torch.load(cfg.TANGWANG_MODEL_PATH, map_location='cpu')
        self.checkpoint_model = self.checkpoint['model']
        self.state_dict = self.model.state_dict()
        for 