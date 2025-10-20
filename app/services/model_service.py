import time
import pickle
import pandas as pd
from app.models.data_models import HouseInput
from app.config.api_model_config import APIPredictConfig
from core.logger import get_logger


class ModelService:
    """
    Service responsible for loading the model and demographics,
    processing input data, and returning house price predictions.
    """

    def __init__(self, config: APIPredictConfig):
        self.config = config
        self.logger = get_logger(__name__)
        
        # Load trained model
        try:
            with open(self.config.model_path, "rb") as f:
                self.model = pickle.load(f)
        except Exception as e:
            raise RuntimeError(f"Error loading model: {e}")

        # Load list of model features
        self.model_features = pd.read_json(self.config.model_features_path, typ='series').tolist()

        # Load demographics dataset
        self.demographics = pd.read_csv(
            self.config.demographics_path,
            dtype={self.config.feature_to_join: str}
        )

    def predict(self, input_data: HouseInput):
        """
        Receives validated input, augments it with demographics,
        and returns prediction + metadata.
        """
        start = time.time()

        df = pd.DataFrame([input_data.model_dump()])

        sample = df.merge(self.demographics, how="left", on=self.config.feature_to_join)

        if sample.isnull().all(axis=1).any():
            raise ValueError(
                f"Demographic data not found for provided {self.config.feature_to_join}: {sample[self.config.feature_to_join].iloc[0]}"
            )

        # Drop join feature (e.g., 'zipcode')
        sample = sample.drop(columns=[self.config.feature_to_join])

        self.logger.debug(f"Missing values per column: {df.isna().sum()}")

        sample.fillna(0, inplace=True)

        # Ensure only expected features are used
        sample = sample[self.model_features]

        prediction = self.model.predict(sample)[0]
        elapsed = round(time.time() - start, 4)

        return {
            "prediction": round(prediction, 2),
            "model_version": self.config.model_version,
            "elapsed_time": elapsed
        }
