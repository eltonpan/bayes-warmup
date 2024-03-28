import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

qm9 = pd.read_csv('data/qm9.csv') # qm9 dataset
qm9['gap'] = qm9['gap']*27.2114

def smiles2gap(smiles):
    if len(qm9[qm9['smiles']==smiles].gap) != 1:
        return qm9[qm9['smiles']==smiles].gap.sample(1).item()
    else:
        return qm9[qm9['smiles']==smiles].gap.item()

def load_results(feat_type, split, n_sample, seed):
    df = pd.read_csv(f'saving/{feat_type}/{split}/{n_sample}/s{seed}.csv')
    df['gap'] = df['smiles'].apply(smiles2gap)

    return df

def get_trajectory(feat_type, split, n_sample):
    dfs = [load_results(feat_type, split, n_sample, seed) for seed in range(10)]

    best_gap_trajs = [] # 10 trajectories of best gaps over iterations for all seeds
    incomplete_seeds = 0
    for df in dfs:
        best_gap_traj = [] # 1 trajectory of best gaps over iterations
        best_gap = 1e3 # initialize best gap with a large number
        for smiles, gap in zip(df['smiles'], df['gap']):
            if gap < best_gap:
                best_gap = gap # update best gap
            best_gap_traj.append(best_gap)
        if len(best_gap_traj) == 50: # some trajectories were not complete
            best_gap_trajs.append(best_gap_traj)
        else:
            incomplete_seeds += 1
    
    print(f'{feat_type}, {split}, {n_sample} non-complete seeds:', incomplete_seeds)
    
    return np.array(best_gap_trajs)

if __name__ == '__main__':
    get_trajectory('morgan', 'random', '20')
