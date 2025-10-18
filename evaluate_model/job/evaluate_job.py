from evaluate_model.task.evaluate import EvaluateModelTask
from evaluate_model.job.config import EvaluateModelJobConfig
from core.logger import get_logger

class EvaluateModelJob:

    def __init__(self, config: EvaluateModelJobConfig):
        self.config = config
        self.evaluation_task = EvaluateModelTask(config=self.config.evaluation_config)
        self.logger = get_logger(__name__)

    def run(self):
        metrics = self.evaluation_task.run()
        return metrics

