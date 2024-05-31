from enum import Enum
import src.config as cfg
from ..model.unet import Unet

class WuguanzhuModelScale(Enum):
    SMALL = 0
    LARGE = 1

class WuguanzhuModel:
    def __init__(self, use_cuda=False):
        self.numClasses = 2
        self.useCuda = use_cuda
        self.smallModel = None
        self.largeModel = None

        # self.load()

    def load(self):
        self.smallModel = Unet(
            model_path=cfg.SMALL_MODEL_PATH, 
            num_classes=self.numClasses,
            backbone='vgg',
            input_shape=[512, 512],
            mix_type = 0, 
            cuda=self.useCuda
        )
        self.largeModel = Unet(
            model_path=cfg.LARGE_MODEL_PATH,
            num_classes=self.numClasses,
            backbone='vgg',
            input_shape=[1024, 1024],
            mix_type = 0,
            cuda=self.useCuda
        )
        
    def getSmallModel(self):
        return self.smallModel
    
    def getLargeModel(self):
        return self.largeModel