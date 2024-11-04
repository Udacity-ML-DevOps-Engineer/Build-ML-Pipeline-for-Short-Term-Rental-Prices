# Build an ML Pipeline for Short-Term Rental Prices in NYC
You are working for a property management company renting rooms and properties for short periods of time on various rental platforms. You need to estimate the typical price for a given property based on the price of similar properties. Your company receives new data in bulk every week. The model needs to be retrained with the same cadence, necessitating an end-to-end pipeline that can be reused.

The project buils the pipeline using MLflow and Weigh & Biases.

## Project Steps

### Create environment
Make sure to have conda installed and ready, then create a new environment using the ``environment.yml``
file provided in the root of the repository and activate it:

```bash
> conda env create -f environment.yml
> conda activate nyc_airbnb_dev
```

### Get API key for Weights and Biases
Let's make sure we are logged in to Weights & Biases. Get your API key from W&B by going to 
[https://wandb.ai/authorize](https://wandb.ai/authorize) and click on the + icon (copy to clipboard), then paste your key into this command:

```bash
> wandb login [your API key]
```

### Running the entire pipeline or just a selection of steps
In order to run the pipeline when you are developing, you need to be in the root of the starter kit, then you can execute as usual:

```bash
>  mlflow run .
```
This will run the entire pipeline.

When developing it is useful to be able to run one step at the time. Say you want to run only
the ``download`` step. The `main.py` is written so that the steps are defined at the top of the file, in the 
``_steps`` list, and can be selected by using the `steps` parameter on the command line:

```bash
> mlflow run . -P steps=download
```
If you want to run the ``download`` and the ``basic_cleaning`` steps, you can similarly do:
```bash
> mlflow run . -P steps=download,basic_cleaning
```

You can override any other parameter in the configuration file using the Hydra syntax, by
providing it as a ``hydra_options`` parameter. For example, say that we want to set the parameter
modeling -> random_forest -> n_estimators to 10 and etl->min_price to 50:

```bash
> mlflow run . \
  -P steps=download,basic_cleaning \
  -P hydra_options="modeling.random_forest.n_estimators=10 etl.min_price=50"
```

### Train the model on a new data sample

Let's now test that we can run the release using ``mlflow`` without any other pre-requisite. We will train the model on a new sample of data that our company received (``sample2.csv``):

```bash
> mlflow run https://github.com/[your github username]/build-ml-pipeline-for-short-term-rental-prices.git \
             -v [the version you want to use, like 1.0.0] \
             -P hydra_options="etl.sample='sample2.csv'"
```

### Optimize HyperParameters

Re-run the entire pipeline varying the hyperparameters of the Random Forest model. This can be
accomplished easily by exploiting the Hydra configuration system. 

```bash
> mlflow run . \
  -P steps=train_random_forest \
  -P hydra_options=" modeling.max_tfidf_features=10,15,30 modeling.random_forest.max_features=0.1,0.33,0.5,0.75,1.0 -m"
```

### Weight & Biases Workspace

All the projects and artifacts can be viewed on the following workspace

```
    https://wandb.ai/samhmariam/nyc_airbnb?nw=nwusersamhmariam
```

