from evaluate_model.task.config import EvaluateModelConfig

from evaluate_model.job.config import EvaluateModelJobConfig
from evaluate_model.job.evaluate_job import EvaluateModelJob

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

evaluate_model_job_config = EvaluateModelJobConfig(
    evaluation_config = evaluate_model_config
)

evaluate_model_job = EvaluateModelJob(
    config=evaluate_model_job_config
)
evaluate_model_job.run()