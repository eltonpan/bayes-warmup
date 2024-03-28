import os
import argparse
import pandas as pd
import numpy as np
from tqdm import tqdm
from sklearn.ensemble import RandomForestRegressor
from multiprocessing import Pool
from scipy.stats import norm
from itertools import repeat

def run(data_path, save_path, test_path):
    files_to_iterate = os.listdir(data_path)
    amounts = [5, 10, 20, 50, 100, 200]
    file_dict = {}
    df_test = pd.read_csv(test_path)
    for a in amounts:
        file_dict[a] = []
    for i in files_to_iterate:
        for amount in amounts:
            if i.split("_")[1][1:] == str(amount):
                file_dict[amount].append(i)

    results = []
    for key, val in file_dict.items():
        file_paths = val
        with Pool(processes=5) as p:
            results.append(
                p.starmap(
                    experiment,
                    zip(
                        file_paths,
                        repeat(data_path),
                        repeat(df_test),
                        repeat(save_path),
                        repeat(key),
                    ),
                )
            )


def experiment(
    file_name,
    data_path,
    df_test,
    save_path,
    key
):
    ind = file_name.split("_")[-1]

    df = pd.read_csv(f"{data_path}/{file_name}")

    finger_type = data_path.split("/")[2]
    print(f"Running {finger_type}")
    if finger_type == "morgan":
        feat_cols = [f"bit{i}" for i in range(2048)]
    elif finger_type == "molformer":
        feat_cols = [f"mf{i}" for i in range(768)]

    vals = df.gap.values

    fingers = df[feat_cols].values
    test_smiles = df_test.smiles.values
    test_fing = df_test[feat_cols].values
    test_vals = df_test.gap.values

    sugg_fingers = []
    sugg_smiles = []

    for j in range(50):
        preds = []
        print(f"Iteration {j} for split {file_name}")
        for i in range(10):
            regr = RandomForestRegressor(random_state=i)
            regr.fit(fingers, vals)
            prediction = regr.predict(test_fing)
            preds.append(prediction)

        prediction = np.array(preds).mean(axis=0)
        uncertainty = np.array(preds).std(axis=0)

        new_point, index = acquisition_function(
            kind="EI",
            prediction=prediction,
            uncertainty=uncertainty,
        )
        # cleanup
        del new_point, prediction, uncertainty

        fingers = np.concatenate((fingers, test_fing[index].reshape(1, -1)))
        vals = np.append(vals, test_vals[index])
        sugg_fingers.append(test_fing[index])
        sugg_smiles.append(test_smiles[index])

        test_fing = np.delete(test_fing, index, axis=0)
        test_vals = np.delete(test_vals, index)
        test_smiles = np.delete(test_smiles, index)

    df_save = pd.DataFrame(np.array(sugg_fingers), columns=feat_cols)
    df_save["smiles"] = sugg_smiles
    df_save = df_save.set_index(["smiles"])
    if not os.path.isdir(f"{save_path}/{key}"):
        os.makedirs(f"{save_path}/{key}")
    df_save.to_csv(f"{save_path}/{key}/{ind}")
    print(f"{key}_{ind} is done")
    # cleanup
    del preds, regr

    return f"{key}_{ind} is done"


def acquisition_function(kind, prediction, uncertainty):
    if kind == "EI":
        ind = expected_improvement(prediction, uncertainty, prediction.min())
    return prediction[ind], ind


def expected_improvement(mean, sigma, ymin):
    u = (mean - ymin) / sigma
    ei = sigma * (u * norm.cdf(u) + norm.pdf(u))
    ei[sigma <= 0] = 0
    return ei.argmin()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Running AL loop for warmstarts")
    parser.add_argument(
        "--data_path",
    )
    parser.add_argument(
        "--save_path",
    )
    parser.add_argument(
        "--test_path",
    )
    args = parser.parse_args()
    run(data_path=args.data_path, save_path=args.save_path, test_path=args.test_path, )

