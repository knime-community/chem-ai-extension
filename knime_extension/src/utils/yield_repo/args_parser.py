from argparse import Namespace

def prepare_args():
    args = Namespace()
    args.bias=True
    args.dataset_type='regression' 
    args.activation='LeakyReLU'
    args.depth=1
    args.depth_diff=1
    args.atom_messages=False
    args.diff_hidden_size=1024
    args.freeze_mpn=False
    args.freeze_mpn_diff=False
    args.gpu=None
    args.dropout=0.1
    args.ensemble_size=1
    args.features_size = 400
    args.features_dim=400
    args.features_only=False
    args.ffn_hidden_size=1024 
    args.ffn_num_layers=3
    args.undirected=False
    args.task_names=['YIELD']
    args.reaction=True
    args.no_cache=False, 
    args.no_features_scaling=False
    args.num_folds=1
    args.num_lrs=1
    args.num_tasks=1 
    args.output_size=1
    args.hidden_size=1024
    args.explicit_hydrogens = False
    args.use_input_features=[r'/content/drive/MyDrive/RnD/separate_classes/train_cv_274090_feat_rdkit.csv']
    args.checkpoint_paths = [r'weights\separate_classes_fixed_features\model_for_class_38\fold_0\model_0\model.pt']
    return args
