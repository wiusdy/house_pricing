from build_model.job.config import BuildModelJobConfig
from build_model.task.create_model import BuildModelTask
from core.logger import get_logger

class BuildModelJob:
    def __init__(self):
        self.logger = get_logger(__name__)
        self.build_model_task = BuildModelTask()

    def run(
            self,
            config: BuildModelJobConfig,
    ) -> None:
        self.logger.info("Starting Build Model Job")
        self.build_model_task.run(config=config.build_model_config)