# 1. Base image with Miniconda
FROM continuumio/miniconda3

# 2. Set working directory inside the container
WORKDIR /app

# 3. Copy environment.yml to container
COPY environment.yml .

# 4. Create the conda environment from environment.yml
RUN conda env create -f environment.yml

# 5. Copy all source code into container
COPY . .

# 6. Copy data and model files
COPY data/zipcode_demographics.csv /app/data/
COPY model/model.pkl /app/model/
COPY model/model_features.json /app/model/

# 7. Copy .env.docker and renomear para .env para facilitar o load
COPY .env.docker /app/.env

# 8. Create directories if needed
RUN mkdir -p /app/data /app/model

# 9. Set PYTHONPATH environment variable so Python can find your package
ENV PYTHONPATH=/app

# 10. Defina variável para seu código saber que está rodando no docker
ENV RUNNING_IN_DOCKER=true

# 11. Run the build_model.py script with the conda environment activated and PYTHONPATH set
RUN /bin/bash -c "source /opt/conda/etc/profile.d/conda.sh && conda activate housing && python -m build_model.build_model"

# 12. Expose port where the API will listen
EXPOSE 8000

# 13. Start the API server with conda env activated and PYTHONPATH set
CMD ["/bin/bash", "-c", "source /opt/conda/etc/profile.d/conda.sh && conda activate housing && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
