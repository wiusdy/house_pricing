from evaluate_model.task.config import EvaluateModelConfig
from pydantic import BaseModel

class EvaluateModelJobConfig(BaseModel):
    evaluation_config: EvaluateModelConfig