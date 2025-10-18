from pydantic import BaseModel
from house_price_estimation.build_model.task.config import BuildModelTaskConfig

class BuildModelJobConfig(BaseModel):
    build_model_config: BuildModelTaskConfig
