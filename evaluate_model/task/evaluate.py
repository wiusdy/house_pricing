import joblib
import json
import pandas
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error
from sklearn import model_selection
from typing import Tuple, Any, Dict, List
from evaluate_model.task.config import EvaluateModelConfig
from core.logger import get_logger


class EvaluateModelTask:

    def __init__(self, config: EvaluateModelConfig):
        self.logger = get_logger(__name__)
        self.config = config

    def _load_model(self) -> Any:
        """
        Load a trained model from a file.

        Returns:
            Any: The loaded model object.
        """
        self.logger.info(f"Loading model from {self.config.model_path}")
        return joblib.load(self.config.model_path)


    def _load_features(self) -> List[str]:
        """
        Load model features metadata from a JSON file.

        Returns:
            List[str]: List containing feature names used by the model.
        """
        self.logger.info(f"Loading model features from {self.config.features_path}")
        with open(self.config.features_path, 'r') as f:
            features = json.load(f)
        if not isinstance(features, list):
            raise ValueError(f"Expected a list of features but got {type(features)}")
        return features

    def _load_data(self) -> Tuple[pandas.DataFrame, pandas.Series]:
        """
        Load dataset by merging sales data with demographics.

        Returns:
            Tuple[pandas.DataFrame, pandas.Series]: Features dataframe and target series.
        """
        self.logger.info(f"Loading sales data from {self.config.sales_path}")
        data = pandas.read_csv(self.config.sales_path, usecols=self.config.sales_column_selection, dtype=self.config.data_dtype)
        self.logger.info(f"Loading demographics data from {self.config.demographics_path}")
        demographics = pandas.read_csv(self.config.demographics_path, dtype=self.config.data_dtype)

        self.logger.info("Merging sales data with demographics")
        merged_data = data.merge(demographics, how="left", on=self.config.feature_to_join).drop(columns=self.config.feature_to_join)

        y = merged_data.pop(self.config.target_column)
        X = merged_data

        return X, y

    def _split_data(
            self, 
            X: pandas.DataFrame,
            Y: pandas.Series,
    ) -> Tuple[pandas.DataFrame, pandas.DataFrame, pandas.Series, pandas.Series]:
        """
        Split the data into training and testing subsets.

        Returns:
            Tuple containing train and test splits of X and Y.
        """
        return model_selection.train_test_split(X, Y, test_size=self.config.test_size, random_state=self.config.random_state)

    def evaluate_model(self, model: Any, X, y) -> Tuple[float, float, float]:
        """
        Evaluate the model's performance on given data.

        Args:
            model (Any): Trained model with a predict method.
            X: Features data (pandas DataFrame or numpy array).
            y: True target values (pandas Series or numpy array).

        Returns:
            Tuple[float, float, float]: (Mean Absolute Error, R2 score, Root Mean Squared Error)
        """
        preds = model.predict(X)
        mae = mean_absolute_error(y, preds)
        r2 = r2_score(y, preds)
        rmse = mean_squared_error(y, preds, squared=False)  # RMSE

        self.logger.info("Model evaluation completed.")
        self.logger.info(f"Mean Absolute Error (MAE): {mae}")
        self.logger.info(f"R-squared (R2): {r2}")
        self.logger.info(f"Root Mean Squared Error (RMSE): {rmse}")

        return mae, r2, rmse

    def run(self) -> Dict[str, float]:
        """
        Run the full evaluation pipeline:
        - Load model and features metadata
        - Load and split data
        - Evaluate model on test data

        Returns:
            dict: Dictionary with metric names and their values.
        """
        self.logger.info("Starting evaluation task")

        model = self._load_model()
        features = self._load_features()
        X, y = self._load_data()

        # Optionally filter X to keep only columns in features
        X = X[features]

        X_train, X_test, y_train, y_test = self._split_data(X, y)

        mae, r2, rmse = self.evaluate_model(model, X_test, y_test)

        metrics = {
            "mae": mae,
            "r2": r2,
            "rmse": rmse,
        }

        self.logger.info(f"Evaluation metrics: {metrics}")

        return metrics
