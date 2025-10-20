from pydantic import BaseModel
from typing import List, Dict

class EvaluateModelConfig(BaseModel):
    sales_path: str
    sales_column_selection: List[str]
    target_column: str
    model_path: str
    features_path: str
    demographics_path: str
    data_dtype: Dict[str, str]
    feature_to_join: str
    test_size: float
    random_state: int