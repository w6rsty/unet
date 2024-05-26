from ..model.unet import Unet
import src.config as cfg


class XuewangModel:
    def __init__(self, use_cuda=False):
        self.numClasses = 2
        self.useCuda = use_cuda
        self.model = None

        self.load()

    def load(self):
        self.model = Unet(
            model_path=cfg.XUEWANG_MODEL_PATH, 
            num_classes=self.numClasses,
            backbone='vgg', 
            input_shape=[1024, 1024],
            mix_type = 2, 
            cuda=self.useCuda
        )
        
    def getModel(self):
        return self.model