from enum import Enum
from .unet import Unet
import config as cfg

class ModelScale(Enum):
    SMALL = 0
    LARGE = 1

class Model:
    async def __init__(self, use_cuda=False):
        self.numClasses = 2
        self.useCuda = use_cuda
        self.smallModel = None
        self.largeModel = None

        await self.load()

    async def load(self):
        self.smallModel = Unet(model_path=cfg.SMALL_MODEL_PATH, num_classes=self.numClasses, input_shape=[512, 512], cuda=self.useCuda)
        self.largeModel = Unet(model_path=cfg.LARGE_MODEL_PATH, num_classes=self.numClasses, input_shape=[1024, 1024], cuda=self.useCuda)
        
    def getSmallModel(self):
        return self.smallModel
    
    def getLargeModel(self):
        return self.largeModel