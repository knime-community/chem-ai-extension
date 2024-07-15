from argparse import Namespace

import numpy as np
import torch

from utils.yield_repo.args_parser import prepare_args
from utils.yield_repo.data_preparation import DataPreparation
from utils.yield_repo.chemprop.utils import load_checkpoint, load_scalers

class YieldInference:
    def __init__(self,
                 REAGENTSMI1: str = None,
                 REAGENTSMI2: str = None,
                 REAGENTSMI3: str = None,
                 PRODUCTSMI: str = None,
                 model_weights: str = None) -> None:
        self.model_weights = model_weights
        self.data_prep = DataPreparation(REAGENTSMI1=REAGENTSMI1,
                                         REAGENTSMI2=REAGENTSMI2,
                                         REAGENTSMI3=REAGENTSMI3,
                                         PRODUCTSMI=PRODUCTSMI)
        
    def predict(self):

        args = prepare_args()
        scaler, _ = load_scalers(self.model_weights)

        model = load_checkpoint(path=self.model_weights,
                                current_args=args,
                                cuda=False)
        

        model.eval()
        
        FEATURES_list = [np.array(self.data_prep.FEATURES.split(','), dtype='float32')]
        REAGENT = (self.data_prep.MAPPED_REAGENT, )
        PRODUCT = (self.data_prep.MAPPED_PRODUCT, )

        with torch.no_grad():
            batch_preds, _, _, _ = model(REAGENT, PRODUCT, FEATURES_list)

            if scaler is not None:
                batch_preds = scaler.inverse_transform(batch_preds)

        return batch_preds[0]
