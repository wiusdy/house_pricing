from build_model.task.config import BuildModelTaskConfig

from build_model.job.config import BuildModelJobConfig
from build_model.job.build_model import BuildModelJob

build_model_task_config = BuildModelTaskConfig(
    sales_path="/home/wiusdy/PhData/house_price_estimation/data/kc_house_data.csv",
    demographics_path="/home/wiusdy/PhData/house_price_estimation/data/zipcode_demographics.csv",
    sales_column_selection=[
        'price', 'bedrooms', 'bathrooms', 'sqft_living', 'sqft_lot', 'floors',
        'sqft_above', 'sqft_basement', 'zipcode'
    ],
    model_output_path="/home/wiusdy/PhData/house_price_estimation/model/",
    data_dtype={
        "zipcode": "str"
    },
    feature_to_join="zipcode",
    target_column="price",
    model_name_output="model.pkl",
    features_name_output="model_features.json"
)

build_model_job_config = BuildModelJobConfig(
    build_model_config=build_model_task_config
)

build_model_job = BuildModelJob()
build_model_job.run(
    config=build_model_job_config,
)
