import os
import enum

PATH_TO_MODEL_WEIGHTS = os.path.join('utils', 'yield_repo', 'weights')
# r'C:\work\DrugDiscovery\fluoricLogPpKa_KNIME_PYTHON_NODE\github_repository\fluoricLogPpKa_KNIME\knime_extension\src\utils\yield_repo\weights\model_for_class_38\model.pt'
class YieldModelWeights(enum.Enum):
    CLASS_20 = os.path.join(PATH_TO_MODEL_WEIGHTS, 'model_for_class_20', 'model.pt')
    CLASS_34 = os.path.join(PATH_TO_MODEL_WEIGHTS, 'model_for_class_34', 'model.pt')
    CLASS_38 = os.path.join(PATH_TO_MODEL_WEIGHTS, 'model_for_class_38', 'model.pt')
    CLASS_207 = os.path.join(PATH_TO_MODEL_WEIGHTS, 'model_for_class_207', 'model.pt')
    CLASS_512 = os.path.join(PATH_TO_MODEL_WEIGHTS, 'model_for_class_512', 'model.pt')
    CLASS_527 = os.path.join(PATH_TO_MODEL_WEIGHTS, 'model_for_class_527', 'model.pt')
    CLASS_2714 = os.path.join(PATH_TO_MODEL_WEIGHTS, 'model_for_class_2714', 'model.pt')
    CLASS_270942 = os.path.join(PATH_TO_MODEL_WEIGHTS, 'model_for_class_270942', 'model.pt')
    CLASS_271570 = os.path.join(PATH_TO_MODEL_WEIGHTS, 'model_for_class_271570', 'model.pt')
    CLASS_274090 = os.path.join(PATH_TO_MODEL_WEIGHTS, 'model_for_class_274090', 'model.pt')
