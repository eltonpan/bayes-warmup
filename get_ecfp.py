import pandas as pd
import numpy as np
import pickle
from rdkit import Chem
from featurizers.morgan import ECFP6

df = pd.read_csv('data/qm9.csv')

ecfp6_descriptor = ECFP6(df['smiles'])
ecfp6_descriptor.compute_ECFP6('data/morgan/qm9.csv')

embeddings_df = pd.read_csv('data/morgan/qm9_ECFP6.csv')
gap_list = df["gap"].tolist()
embeddings_df["gap"] = gap_list
embeddings_df["gap"] = embeddings_df["gap"]*27.2114
embeddings_df.to_csv('data/qm9_ECFP6.csv')
