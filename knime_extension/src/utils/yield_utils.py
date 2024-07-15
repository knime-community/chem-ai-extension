from utils.yield_repo.inference import YieldInference

def predict_yield(REAGENTSMI1: str = None,
                  REAGENTSMI2: str = None,
                  REAGENTSMI3: str = None,
                  PRODUCTSMI: str = None,
                  model_weights: str = None,
                  execution_context=None,
                  index: int = None,
                  total_number_of_operations: int = None) -> float:

    full_reaction = f"{REAGENTSMI1}, {REAGENTSMI2}, {PRODUCTSMI}"
    if REAGENTSMI3 is not None:
        full_reaction = f"{REAGENTSMI1}, {REAGENTSMI2}, {REAGENTSMI3}, {PRODUCTSMI}"

    if execution_context is not None:
        execution_context.set_progress(progress=(index + 1)/total_number_of_operations,
                                       message=f"Features generating for: {full_reaction}")
        
    inference_yield = YieldInference(REAGENTSMI1=REAGENTSMI1, REAGENTSMI2=REAGENTSMI2, REAGENTSMI3=REAGENTSMI3, PRODUCTSMI=PRODUCTSMI, model_weights=model_weights)
    
    if execution_context is not None:
        execution_context.set_progress(progress=(index + 2)/total_number_of_operations,
                                       message=f"pKa prediction for: {full_reaction}")
    
    return inference_yield.predict()[0]