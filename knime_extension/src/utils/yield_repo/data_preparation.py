import pandas as pd
from rdkit import Chem
from indigo import Indigo, IndigoException

from utils.yield_repo.descriptastorus.descriptors import rdNormalizedDescriptors

class DataPreparation:
    def __init__(self,
                 REAGENTSMI1: str = None,
                 REAGENTSMI2: str = None,
                 REAGENTSMI3: str = None,
                 PRODUCTSMI: str = None) -> None:
        
        REACTION = DataPreparation.make_reaction_smiles(REAGENTSMI1=REAGENTSMI1, REAGENTSMI2=REAGENTSMI2, REAGENTSMI3=REAGENTSMI3, RESULT_SMILES=PRODUCTSMI)
        REACTION_SHORT = DataPreparation.make_short_reaction_smiles(REAGENTSMI1=REAGENTSMI1, REAGENTSMI2=REAGENTSMI2, REAGENTSMI3=REAGENTSMI3, RESULT_SMILES=PRODUCTSMI)

        MAPPED_REACTION = DataPreparation.complete_atom_mapping(DataPreparation.map_r(REACTION_SHORT))

        self.MAPPED_REAGENT = MAPPED_REACTION.split('>>')[0]
        self.MAPPED_PRODUCT = MAPPED_REACTION.split('>>')[1]

        self.FEATURES = DataPreparation.generate_features(REAGENTSMI1=REAGENTSMI1, REAGENTSMI2=REAGENTSMI2, REAGENTSMI3=REAGENTSMI3)
    
    @staticmethod
    def make_reaction_smiles(REAGENTSMI1: str = None, 
                         REAGENTSMI2: str = None, 
                         REAGENTSMI3: str = None,
                         RESULT_SMILES: str = None):

        precursors = f"{REAGENTSMI1}.{REAGENTSMI2}"
        if REAGENTSMI3 is not None: precursors += f".{REAGENTSMI3}"

        product = RESULT_SMILES
        can_precursors = Chem.MolToSmiles(Chem.MolFromSmiles(precursors.replace('...', '.').replace('..', '.').replace(' .', '').replace('. ', '').replace(' ', '')))
        can_product = Chem.MolToSmiles(Chem.MolFromSmiles(product))
        
        return f"{can_precursors}>>{can_product}"
    
    @staticmethod
    def make_short_reaction_smiles(REAGENTSMI1: str = None, 
                               REAGENTSMI2: str = None, 
                               REAGENTSMI3: str = None,
                               RESULT_SMILES: str = None):
        precursors = f"{REAGENTSMI1.split('.')[0]}.{REAGENTSMI2.split('.')[0]}" 
        if REAGENTSMI3 is not None: precursors += f".{REAGENTSMI3.split('.')[0]}"
        
        product = RESULT_SMILES
        
        can_precursors = Chem.MolToSmiles(Chem.MolFromSmiles(precursors.replace('...', '.').replace('..', '.').replace(' .', '').replace('. ', '').replace(' ', '')))
        can_product = Chem.MolToSmiles(Chem.MolFromSmiles(product))
        
        return f"{can_precursors}>>{can_product}"
    
    @staticmethod
    def map_r(row):
        try:
            r = Indigo().loadReaction(row)
            r.automap("discard")
        except IndigoException as e:
            return None
        return r.smiles()
    
    @staticmethod
    def complete_atom_mapping(r):
        """
        Add atoms to the reaction SMILES which aren't in the main product but are present in the reactants or vice versa 
        and asigns indices to them. A workaround which enables to use difference D-MPNN with incomplete reaction SMILES.
        """
        global count
        if pd.isnull(r):
            return None
        str_r, str_p = r.split('>>')
        mr = Chem.MolFromSmiles(str_r)
        mp = Chem.MolFromSmiles(str_p)
        
        for m in [mr, mp]:
            unique_indices = [0]
            for a in m.GetAtoms():
                if a.GetAtomMapNum() in unique_indices:
                    a.SetAtomMapNum(0)
                else:
                    unique_indices.append(a.GetAtomMapNum())

        unmapped_symbols_r = [a  for a in mr.GetAtoms() if a.GetAtomMapNum() == 0]
        unmapped_symbols_p = [a  for a in mp.GetAtoms() if a.GetAtomMapNum() == 0]
        #maybe add some kind of substucture mapping
        str_to_add_r, str_to_add_p = '', ''
        max_indx = max(max([a.GetAtomMapNum() for a in mr.GetAtoms()]), max([a.GetAtomMapNum() for a in mp.GetAtoms()]))
        for a_r in unmapped_symbols_r:
            was_mapped = False
            s_r = a_r.GetSymbol()
            a_r.SetAtomMapNum(max_indx + 1)
            for i, a_p in enumerate(unmapped_symbols_p):
                if s_r == a_p.GetSymbol():
                    a_p.SetAtomMapNum(max_indx + 1)
                    unmapped_symbols_p.pop(i)
                    was_mapped = True
                    break
            
            if not was_mapped:
                str_to_add_p += f'.[{a_r.GetSymbol()}:{max_indx + 1}]'
            max_indx += 1
        
        for a_p in unmapped_symbols_p:
            a_p.SetAtomMapNum(max_indx + 1)
            str_to_add_r += f'.[{a_p.GetSymbol()}:{max_indx + 1}]'
            max_indx += 1
        
        str_r = Chem.MolToSmiles(mr) + str_to_add_r
        str_p = Chem.MolToSmiles(mp) + str_to_add_p
        
        if (not Chem.MolFromSmiles(str_r)) or (not Chem.MolFromSmiles(str_p)):
            return None

        return '>>'.join([str_r, str_p])

    @staticmethod
    def gen_rdkit2d_features(sm):
        generator = rdNormalizedDescriptors.RDKit2DNormalized()
        try:
            features = generator.process(sm)[1:]
        except TypeError as e:
            return [0.] * 200
        return features

    @staticmethod
    def generate_features(REAGENTSMI1: str = None, 
                      REAGENTSMI2: str = None, 
                      REAGENTSMI3: str = None):
        SMILES_to_encode = [REAGENTSMI1, REAGENTSMI2]
        if REAGENTSMI3 is not None: 
            SMILES_to_encode.append(REAGENTSMI3)
        
        return ','.join([','.join(map(str, DataPreparation.gen_rdkit2d_features(c))) for c in SMILES_to_encode])
