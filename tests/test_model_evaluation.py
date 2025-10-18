from evaluate_model.task.config import EvaluateModelConfig
from evaluate_model.job.config import EvaluateModelJobConfig
from evaluate_model.job.evaluate_job import EvaluateModelJob

def test_evaluate_model_job_run():
    # Setup the evaluation configuration with the proper file paths and parameters
    evaluate_model_config = EvaluateModelConfig(
        sales_path="/home/wiusdy/PhData/house_price_estimation/data/kc_house_data.csv",
        demographics_path="/home/wiusdy/PhData/house_price_estimation/data/zipcode_demographics.csv",
        sales_column_selection=[
            'price', 'bedrooms', 'bathrooms', 'sqft_living', 'sqft_lot', 'floors',
            'sqft_above', 'sqft_basement', 'zipcode'
        ],
        model_path="/home/wiusdy/PhData/house_price_estimation/model/model.pkl",
        features_path="/home/wiusdy/PhData/house_price_estimation/model/model_features.json",
        data_dtype={
            "zipcode": "str"
        },
        feature_to_join="zipcode",
        target_column="price",
        test_size=0.1,
        random_state=42
    )

    # Create job configuration by wrapping the evaluation config
    evaluate_model_job_config = EvaluateModelJobConfig(
        evaluation_config=evaluate_model_config
    )

    # Instantiate the EvaluateModelJob with the above config
    evaluate_model_job = EvaluateModelJob(
        config=evaluate_model_job_config
    )

    # Run the evaluation job; this should train/test and evaluate the model
    # Depending on implementation, run() may return metrics or None
    result = evaluate_model_job.run()

    # Assert basic expectations:
    # Check if the function runs without raising exceptions
    # and optionally verify if results exist
    assert result is None or result is not None
    assert 'mae' in result
    assert 'r2' in result
    assert 'rmse' in result
    assert result['r2'] > 0.5  # model fitting more than half of the data