from pydantic import BaseModel
from typing import List, Dict

class BuildModelTaskConfig(BaseModel):
    sales_path: str
    demographics_path: str
    sales_column_selection: List[str]
    model_output_path: str
    data_dtype: Dict[str, str]
    feature_to_join: str
    target_column: str
    model_name_output: str
    features_name_output: str