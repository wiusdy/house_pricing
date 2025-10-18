import json
import pathlib
import pickle
from typing import Tuple

import pandas
from house_price_estimation.build_model.task.config import BuildModelTaskConfig
from house_price_estimation.core.logger import get_logger
from sklearn import model_selection
from sklearn import neighbors
from sklearn import pipeline
from sklearn import preprocessing

class BuildModelTask:
    def __init__(self,):
        self.logger = get_logger(__name__)

    def run(self, config: BuildModelTaskConfig):
        """
        Execute the complete model training pipeline.

        This method performs the following steps:
        1. Loads and preprocesses the dataset.
        2. Splits the data into training and testing sets.
        3. Trains the machine learning model using the training set.
        4. Saves the trained model and associated artifacts to disk.

        Logging messages are emitted throughout the process to track progress
        and help with debugging.

        Args:
            config (CreateModelConfig): Configuration object containing file paths,
                column selections, model parameters, and output settings.

        Returns:
            None
        """

        self.logger.info("Creating the model")
        X, Y = self._load_data(config=config)
        x_train, x_test, y_train, y_test = self._split_data(X=X, Y=Y)
        model = self._make_model(x_train=x_train, y_train=y_train)
        self.logger.info("Model trained successfully! Saving the model now..")
        self._dump_model(model=model, x_train=x_train, config=config)
        self.logger.info("Model creation pipeline finished Successfully!")

    
    def _load_data(
            self,
            config: BuildModelTaskConfig
    ) -> Tuple[pandas.DataFrame, pandas.DataFrame]:
        """Load the target and feature data by merging sales and demographics.

        Args:
            model_create_config: BuildModelTaskConfig

        Returns:
            Tuple containg with two elements: a DataFrame and a Series of the same
            length.  The DataFrame contains features for machine learning, the
            series contains the target variable (home sale price).

        """
        try:
            data = pandas.read_csv(config.sales_path,
                            usecols=config.sales_column_selection,
                            dtype=config.data_dtype)
            demographics = pandas.read_csv(config.demographics_path,
                                        dtype=config.data_dtype)
        except Exception as error:
            self.logger.error(f"Error while loading data to train model -> {error}")
            raise Exception(f"{error}")


        try:
            merged_data = data.merge(demographics, how="left",
                                on=config.feature_to_join).drop(columns=config.feature_to_join)
        except Exception as error:
            self.logger.error(f"Error while merging data -> {error}")
            raise Exception(f"{error}")

        y = merged_data.pop(config.target_column)
        x = merged_data

        return x, y
    
    def _split_data(
            self, 
            X: pandas.DataFrame,
            Y: pandas.DataFrame,
    ) -> Tuple[pandas.DataFrame, pandas.DataFrame, pandas.Series, pandas.Series]:
        return model_selection.train_test_split(X, Y, random_state=42)

    def _make_model(
            self,
            x_train: pandas.DataFrame,
            y_train: pandas.DataFrame
    ) -> pipeline.Pipeline:
        return pipeline.make_pipeline(
            preprocessing.RobustScaler(),
            neighbors.KNeighborsRegressor()).fit(x_train, y_train)
    
    def _dump_model(
            self,
            model: pipeline.Pipeline,
            x_train: pandas.DataFrame,
            config: BuildModelTaskConfig
    ) -> None:
        output_dir = pathlib.Path(config.model_output_path)
        output_dir.mkdir(exist_ok=True)

        # Output model artifacts: pickled model and JSON list of features
        pickle.dump(model, open(output_dir / f"{config.model_name_output}", 'wb'))
        json.dump(list(x_train.columns),
                open(output_dir / f"{config.features_name_output}", 'w'))
