from sklearn.datasets import load_iris, load_diabetes, load_wine
from sklearn.svm import SVC, SVR
from sklearn.linear_model import SGDClassifier, LinearRegression
from sklearn.metrics import f1_score, accuracy_score, root_mean_squared_error, mean_squared_error
from sklearn.model_selection import KFold, StratifiedKFold
import numpy as np

class_metrics = [
    {
        "name": "Acc",
        "func": accuracy_score
    },
    {
        "name": "F1score",
        "func": f1_score
    },
]

regs_metrics = [
    {
        "name": "MSE",
        "func": mean_squared_error
    },
    {
        "name": "RMSE",
        "func": root_mean_squared_error
    },
]

class_models = [
    {
        "name": "SVC",
        "class": SVC,
        "metrics": class_metrics
    },
    {
        "name": "SGDClassifier",
        "class": SGDClassifier,
        "metrics": class_metrics
    }
]

regs_models = [
    {
        "name": "SVR",
        "class": SVR,
        "metrics": regs_metrics
    },
    {
        "name": "SGDClassifier",
        "class": LinearRegression,
        "metrics": regs_metrics
    }
]

exec_params =[
        {
            "name": "Iris",
            "load": load_iris,
            "models": class_models
        },
        {
            "name": "Wine",
            "load": load_wine,
            "models": class_models
        },
        {
            "name": "Diabetes",
            "load": load_diabetes,
            "models": regs_models
        }
    ]

for exec in exec_params:
    print(f"Processando dataset: {exec["name"]}")
    dataset = exec["load"]()
    x = dataset.data
    y = dataset.target

    for model in exec["models"]:
        print(f"Avaliando modelo - {model["name"]}")
        model_obj = model["class"]()
        metrics = []
        for metric in model["metrics"]:
            metrics.append([])

        kf = StratifiedKFold(n_splits=5, shuffle=True)
        for i, (train_index, test_index) in enumerate(kf.split(x, y)):
            model_obj.fit(x[train_index], y[train_index])
            result = model_obj.predict(x[test_index])

            for idx, metric in enumerate(model["metrics"]):
                if metric["name"] == "F1score":
                    metrics[idx].append(metric["func"](y[test_index], result, average="macro"))
                else:
                    metrics[idx].append(metric["func"](y[test_index], result))

        for metric in model["metrics"]:
            print(f"{metric["name"]}: {np.mean(metrics[idx])}")

        print("\n")
