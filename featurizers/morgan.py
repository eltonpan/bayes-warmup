# import numpy as np
# from rdkit.Chem import AllChem
# from ast import literal_eval

# class MorganDictVectorizer(object):
#     '''
#     Morgan fingerprint generator for organic molecules Source: https://programtalk.com/vs4/python/hcji/PyFingerprint/PyFingerprint/heteroencoder.py/
#     '''
#     def __init__(self, radius=2, augment=None):
#         self.radius = radius
#         self.augment = augment #Not used
#         self.dims = None
        
#     def fit(self, mols):
#         """Analyses the molecules and creates the key index for the creation of the dense array"""
#         keys=set()
#         for mol in mols:
#             fp = AllChem.GetMorganFingerprint(mol,self.radius)
#             keys.update(fp.GetNonzeroElements().keys())
#         keys = list(keys)
#         keys.sort()
#         self.keys= np.array(keys)
#         self.dims = len(self.keys)
        
#     def transform_mol(self, mol, misses=False):
#         """ transforms the mol into a dense array using the fitted keys as index
        
#             :parameter mol: the RDKit molecule to be transformed
#             :parameter misses: wheter to return the number of key misses for the molecule
#          """
#         assert type(self.keys) is np.ndarray, "keys are not defined or is not an np.array, has the .fit(mols) function been used?"
#         #Get fingerprint as a dictionary
#         fp = AllChem.GetMorganFingerprint(mol,self.radius)
#         fp_d = fp.GetNonzeroElements()
        
#         #Prepare the array, and set the values
#         #TODO is there a way to vectorize and speed up this?
#         arr = np.zeros((self.dims,))
#         _misses = 0
#         for key, value in fp_d.items():
#             if key in self.keys:
#                 arr[self.keys == key] = value
#             else:
#                 _misses = _misses + 1
        
#         if misses:
#             return arr, _misses
#         else:
#             return arr
    
#     def transform(self, mols, misses=False):
#         """Transforms a list or array of RDKit molecules into a dense array using the key dictionary (see .fit())
        
#         :parameter mols: list or array of RDKit molecules
#         :parameter misses: Wheter to return the number of key misses for each molecule
#         """
#         arr = np.zeros((len(mols), self.dims))
#         if misses:
#             _misses = np.zeros((len(mols),1))
#             for i, mol in enumerate(mols):
#                 arr[i,:], _misses[i] = self.transform_mol(mol, misses=misses)
#             return arr, _misses
#         else:
#             for i, mol in enumerate(mols):
#                 arr[i,:] = self.transform_mol(mol, misses=False)
#             return arr


import numpy as np
import pandas as pd
from rdkit.Chem import AllChem
from rdkit import Chem, DataStructs
import tqdm

class ECFP6:
    def __init__(self, smiles):
        self.mols = [Chem.MolFromSmiles(i) for i in smiles]
        self.smiles = smiles

    def mol2fp(self, mol, radius = 3):
        fp = AllChem.GetMorganFingerprintAsBitVect(mol, radius = radius)
        array = np.zeros((1,))
        DataStructs.ConvertToNumpyArray(fp, array)
        return array

    def compute_ECFP6(self, name):
        bit_headers = ['bit' + str(i) for i in range(2048)]
        arr = np.empty((0,2048), int).astype(int)
        for i in tqdm.tqdm(self.mols):
            fp = self.mol2fp(i)
            arr = np.vstack((arr, fp))
        df_ecfp6 = pd.DataFrame(np.asarray(arr).astype(int),columns=bit_headers)
        df_ecfp6.insert(loc=0, column='smiles', value=self.smiles)
        df_ecfp6.to_csv(name[:-4]+'_ECFP6.csv', index=False)