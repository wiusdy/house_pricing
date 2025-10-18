from pydantic import BaseModel
from build_model.task.config import BuildModelTaskConfig

class BuildModelJobConfig(BaseModel):
    build_model_config: BuildModelTaskConfig
