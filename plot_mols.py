import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
from rdkit import Chem
from matplotlib.colors import LogNorm
from featurizers.morgan import ECFP6
from sklearn.decomposition import PCA

# input your filename
samples = pd.read_csv('samples.csv')
feat_name = 'morgan'

# dataset and featurization
qm9 = pd.read_csv('data/qm9.csv') # qm9 dataset
qm9['gap'] = qm9['gap']*27.2114
if feat_name == 'morgan':
    feat = pd.read_csv(f'data/{feat_name}/qm9_ECFP6.csv')
    feat_cols = [f'bit{i}' for i in range(2048)]
elif feat_name == 'molformer': 
    feat = pd.read_csv(f'data/{feat_name}/qm9_molformer.csv')
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

feat_samples = feat[feat['smiles'].isin(samples['smiles'].tolist())]
feat_samples

fig = plt.figure(figsize=(9,8), dpi=300)
plt.scatter(feat['PCA 1'], feat['PCA 2'], 
            # c=feat['gap'], 
            c=feat['gap'],
            marker='o', s=10, cmap='coolwarm', linewidth=0.1, edgecolors='black', alpha=1.,
            # norm=LogNorm(),
            vmin=np.quantile(feat['gap'], 0.01), vmax=np.quantile(feat['gap'], 0.99),
            )

cb = plt.colorbar()
cb.set_label(label='Gap (eV)', size=20)
cb.ax.tick_params(labelsize=20)
plt.scatter(feat_samples['PCA 1'], feat_samples['PCA 2'], 
            c='g', 
            marker='o', s=100, label='samples', cmap='coolwarm', linewidth=2, edgecolors='black', alpha=1,
            )
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.xlabel('PCA 1', fontsize=20)
plt.ylabel('PCA 2', fontsize=20)
plt.legend(fontsize=20)
plt.savefig(f'PCA.png', dpi=300)
plt.show()