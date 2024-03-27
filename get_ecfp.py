import pandas as pd
import numpy as np
import pickle
from rdkit import Chem
# from featurizers.morgan import MorganDictVectorizer
from featurizers.morgan import ECFP6

df = pd.read_csv('data/qm9.csv')

ecfp6_descriptor = ECFP6(df['smiles'])
ecfp6_descriptor.compute_ECFP6('data/morgan/ECFP6.csv')
