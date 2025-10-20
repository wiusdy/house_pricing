from build_model.task.config import BuildModelTaskConfig
from build_model.job.config import BuildModelJobConfig
from build_model.job.build_model import BuildModelJob

def main():
    # Configurações do build do modelo
    build_model_task_config = BuildModelTaskConfig(
        sales_path="/app/data/kc_house_data.csv",
        demographics_path="/app/data/zipcode_demographics.csv",
        sales_column_selection=[
            'price', 'bedrooms', 'bathrooms', 'sqft_living', 'sqft_lot', 'floors',
            'sqft_above', 'sqft_basement', 'zipcode'
        ],
        model_output_path="/app/model/",
        data_dtype={"zipcode": "str"},
        feature_to_join="zipcode",
        target_column="price",
        model_name_output="model.pkl",
        features_name_output="model_features.json"
    )

    # Config do job
    build_model_job_config = BuildModelJobConfig(
        build_model_config=build_model_task_config
    )

    # Instancia e roda o job de build do modelo
    build_model_job = BuildModelJob()
    build_model_job.run(config=build_model_job_config)

if __name__ == "__main__":
    main()
