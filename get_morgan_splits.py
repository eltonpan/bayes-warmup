import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
from rdkit import Chem
from matplotlib.colors import LogNorm
from featurizers.morgan import ECFP6
from sklearn.decomposition import PCA
from kmeans import get_centroids, get_cluster_id

feat_name = 'morgan'

# dataset and featurization
qm9 = pd.read_csv('data/qm9.csv') # qm9 dataset
qm9['gap'] = qm9['gap']*27.2114
if feat_name == 'morgan':
    feat = pd.read_csv(f'data/qm9_ECFP6.csv')
    feat_cols = [f'bit{i}' for i in range(2048)]
elif feat_name == 'molformer': 
    feat = pd.read_csv(f'data/qm9_molformer.csv')
    feat_cols = [f'mf{i}' for i in range(768)]

# col names
prop_cols = ['A', 'B', 'C', 'mu', 'alpha', 'homo', 'lumo', 'gap',
       'r2', 'zpve', 'u0', 'u298', 'h298', 'g298', 'cv', 'u0_atom',
       'u298_atom', 'h298_atom', 'g298_atom']

# combine features with dataset
for col in prop_cols:
    feat[col] = qm9[col]

# PCA 
pca = PCA(n_components=2)
feat_pca = pca.fit_transform(feat[feat_cols])
feat['PCA 1'], feat['PCA 2']  = feat_pca[:,0], feat_pca[:,1]

# mask out bottom 40% of gaps
percentile = 0.4
feat_masked = feat[feat['gap'] > np.quantile(feat['gap'], percentile)]

# random splits
n_seeds = 10
n_samples = [5, 10, 20, 50, 100, 200]
for n_sample in n_samples:
    for seed in range(n_seeds):
        feat_masked.sample(n_sample, random_state=seed).to_csv(f'data/{feat_name}/splits/random/warmup_n{n_sample}_s{seed}.csv', index=False)

# get centroids and cluster ids for each point
n_centroids = 5
centroids = get_centroids(data=feat_masked[['PCA 1', 'PCA 2']], num_centroids=n_centroids)
cluster_ids = get_cluster_id(feat_masked[['PCA 1', 'PCA 2']], centroids) 
feat_masked['cluster_id'] = cluster_ids

# fragment split
for n_sample in n_samples:
    for cluster_id in range(n_centroids):
        feat_masked_frag = feat_masked[feat_masked['cluster_id'] == cluster_id]
        for seed in range(n_seeds):
            feat_masked_frag.sample(n_sample, random_state=seed).to_csv(f'data/{feat_name}/splits/fragment/warmup_n{n_sample}_c{cluster_id}_s{seed}.csv', index=False)

# stratified split
assert n_sample%n_centroids == 0, 'n_sample must be divisible by n_centroids'
for n_sample in n_samples:
    for seed in range(n_seeds):
        stratified_samples = []
        for cluster_id in range(n_centroids):
            samples = feat_masked[feat_masked['cluster_id'] == cluster_id].sample(int(n_sample/n_centroids), random_state=seed)
            stratified_samples.append(samples)
        stratified_samples = pd.concat(stratified_samples)
        stratified_samples.to_csv(f'data/{feat_name}/splits/stratified/warmup_n{n_sample}_s{seed}.csv', index=False)
