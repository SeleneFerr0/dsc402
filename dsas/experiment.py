import os
import pandas as pd
import numpy as np
import mlflow

from sklearn.model_selection import GridSearchCV

def mlflow_run(experiment_id, estimator, param_grid, data):
    (X_train, X_test, y_train, y_test) = data

    with mlflow.start_run(experiment_id=experiment_id) as run:
        gs = GridSearchCV(estimator, param_grid)
        gs.fit(X_train, y_train)

        train_acc = gs.score(X_train, y_train)
        test_acc = gs.score(X_test, y_test)
        mlflow.log_param("model",
                         (str(estimator.__class__)
                          .split('.')[-1].replace("'>","")))

        mlflow.sklearn.log_model(gs.best_estimator_, "model")

        for param, value in gs.best_params_.items():
            mlflow.log_param(param, value)
        mlflow.log_metric("train acc", train_acc)
        mlflow.log_metric("test acc", test_acc)
        
def prepare_results(experiment_id):
    results = mlflow.search_runs(experiment_id)
    columns = [
      col for col in results.columns
      if any([
        'metric' in col,
        'param' in col,
        'artifact' in col
      ])
    ]
    return results[columns]

def prepare_coefs(experiments, lifestyles, feature_columns):
    # s3://mlflow/1/84e2e9717ce742bc8b99dc71af4388b1/artifacts/model
   
    models = [
      mlflow.sklearn.load_model(artifact_uri + "/model")
      for artifact_uri in experiments['artifact_uri'].values
    ]

    models = [
      {**model.get_params(),
        "coefs" : model.coef_
      } for model in models
    ]
    coefs = pd.DataFrame(models)
    coefs = coefs[["C", "l1_ratio", "penalty", "coefs"]]
    coefs["coefs"] = (
      coefs["coefs"]
      .apply(
        lambda artifact: [
          (lifestyle, coefs)
          for lifestyle, coefs
          in zip(lifestyles, artifact)
        ]
      )
    )
    coefs = coefs.explode("coefs")
    coefs["lifestyle"] = coefs["coefs"].apply(lambda artifact: artifact[0])
    coefs["coefs"] = coefs["coefs"].apply(lambda artifact: artifact[1])
    coefs.set_index(["C", "l1_ratio", "penalty", "lifestyle"], inplace=True)
    coefs = coefs["coefs"].apply(pd.Series)
    coefs.columns = feature_columns
    ax = coefs.T.plot(figsize=(20,7))
    ax.set_xticks(range(len(coefs.columns)));
    ax.set_xticklabels(coefs.columns.tolist(), rotation=45)
    return coefs, ax