
# House Price Estimation - Setup & Execution Guide

This guide provides clear, step-by-step instructions to set up the project environment, run automated tests, build a Docker image, and test the prediction API using Insomnia.


## 1. Clone the Repository  
First, clone the project from GitHub and navigate into the project directory:

```
> git clone https://github.com/wiusdy/house_pricing.git
> cd house_pricing

> git checkout master
> git pull origin master
```

## 2. Create and Activate Conda Environment 
```
> conda env create -f environment.yml
> conda activate housing
```

## 3. Run Unit Tests
```
> pytest
```

## 4. Build Image Docker
```
> docker build -t house_price_estimation .

> docker run -p 8000:8000 house_price_estimation
```
## 5. Execute system with Insomnia
Open the Insomnia system, create a POST request using:

```
> http://localhost:8000/predict
```

Use this body in the POST request: 

```
{
    "bedrooms": 2,
    "bathrooms": 1.0,
    "sqft_living": 900,
    "sqft_lot": 4000,
    "floors": 1.0,
    "sqft_above": 900,
    "sqft_basement": 0,
    "zipcode": "98001"
}
```