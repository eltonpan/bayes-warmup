import os
import argparse
import pandas as pd
import numpy as np 
from sklearn.ensemble import RandomForestRegressor
from forestci import random_forest_error
from functions import process_df
from multiprocessing import Pool

def run(data_path, save_path, test_path):
    
    files_to_iterate = os.listdir(data_path)
    amounts = [5,10,20,50,100,200]
    file_dict = {}
    df_test = pd.read_csv(test_path)
    for a in amounts:
        file_dict[a] = []
    for i in files_to_iterate:
        for amount in amounts:
            if i.split('_')[1][1:] == str(amount):
                file_dict[amount].append(i)
    
    results = []
    for key, val in file_dict.items():
        # for file_name in val:
        with Pool(10) as p:
            results.append(p.starmap(
                experiment,
                [(f,data_path,df_test,save_path,key) for f in val]
                ))          

def experiment(
    file_name,
    data_path,
    df_test,
    save_path,
    key,
    ):
    ind = file_name.split("_")[-1]
            
    df = pd.read_csv(f"{data_path}/{file_name}")

    feat_cols = [f'bit{i}' for i in range(2048)]
    vals = df.gap.values

    fingers = df[feat_cols].values
    test_smiles = df_test.smiles.values
    test_fing = df_test[feat_cols].values
    test_vals = df_test.gap.values
    
    sugg_fingers = []
    sugg_smiles = []
    
    for j in range(3):
    
        preds = []
        for i in range(10):
            regr = RandomForestRegressor(
                random_state=i
                )
            regr.fit(fingers, vals)
            prediction = regr.predict(test_fing)
            preds.append(prediction)
        
        prediction = np.array(preds).mean(axis=0)
        uncertainty = np.array(preds).std(axis=0)
        # prediction = regr.predict(test_fing)
        # uncertainty = random_forest_error(
        #     regr, 
        #     fingers.shape,
        #     test_fing
        # )
        
        new_point, index = acquisition_function(
            kind="EI", 
            prediction=prediction, 
            uncertainty=uncertainty,
            )

        fingers = np.concatenate((fingers, test_fing[index].reshape(1,-1)))
        vals = np.append(vals, test_vals[index])
        sugg_fingers.append(test_fing[index])
        sugg_smiles.append(test_smiles[index])
        

        test_fing = np.delete(test_fing, index,axis=0)
        test_vals = np.delete(test_vals, index)
        test_smiles = np.delete(test_smiles, index)

    
    df_save = pd.DataFrame(np.array(sugg_fingers), columns=feat_cols)
    df_save['smiles'] = sugg_smiles
    df_save = df_save.set_index(['smiles'])
    if not os.path.isdir(f"{save_path}/{key}"):
        os.makedirs(f"{save_path}/{key}")
    df_save.to_csv(f"{save_path}/{key}/{ind}")
    print(f"{key}_{ind} is done")
    return f"{key}_{ind} is done"
    
    
    
def acquisition_function(kind, prediction, uncertainty):
    return prediction[0], 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Running AL loop for warmstarts"
    )
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
    run(
        data_path=args.data_path,
        save_path=args.save_path,
        test_path=args.test_path
    )