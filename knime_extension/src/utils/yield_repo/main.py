from constants import YieldModelWeights
from inference import YieldInference

REAGENTSMI1 = "Nc1cc(ccc1F)[N+](=O)[O-]"
REAGENTSMI2 = "CC(=O)c1cccc(NC(=O)CCl)c1"
REAGENTSMI3 = None
PRODUCTSMI = "CC(=O)C1=CC=CC(NC(=O)CNC2=CC(=CC=C2F)[N+]([O-])=O)=C1"

if __name__ == "__main__":
    inference = YieldInference(REAGENTSMI1=REAGENTSMI1, REAGENTSMI2=REAGENTSMI2, REAGENTSMI3=REAGENTSMI3, PRODUCTSMI=PRODUCTSMI, model_weights=YieldModelWeights.CLASS_38.value)
    print(inference.predict())

