# AC BO Hackathon 2024: Team `bayes-warmup`

This is the official repository of:

**How does initial warm-up data influence Bayesian optimization in low-data experimental settings**  (AC BO Hackathon 2024)

Elton Pan (MIT), Jurgis Ruza (MIT), Pengfei Cai (MIT)

[Poster](figures/bo_poster.png) | [Video](https://youtu.be/4gPTMaarQt0) | [Social](https://twitter.com/pengfeicsci/status/1776721505361248278)

<p align="center">
  <img src="/figures/bo_trajectory.gif" width="400"/> 
</p>


## 1) Overview

Real-world experiments in chemistry and materials science often involve very small initial datasets (10-100 data points). In this project, we propose to investigate **how the 1) size and 2) distribution of the warm-up dataset** influence the performance of bayesian optimization. We propose experiments on **HOMO-LUMO gap minimization** task using the well-known **QM9 dataset**.

## 2) Main findings

<p align="center">
<img src="/figures/stratified.png" width="350"/> 
</p>

### A) Stratified sampling is more efficient than random
First, a k-means clustering algorithm determines the centroids (green), resulting in clusters shown above. Stratified sampling (i.e. sampling same number of datapoints per cluster) is then performed. For example, if we want to sample 10 warmup datapoints, we can sample 2 samples per cluster (see above). We show that stratified sampling as a more efficient way to sample a warmup dataset (right, `molformer-stratified` vs. `molformer random`). 


<p align="center">
  <img src="/figures/bo_results.png" width="900"/> 
</p>

### B) Pretrained embeddings allow more efficient exploration in low-data regimes
Here, we vary the number of datapoints from 5-200. We show that simple representations such as Morgan fingerprints (left), more warmup samples improves BO performance. However, this is not true for pretrained embeddings such as MolFormer (center), where **more warmup datapoints do not necessarily improve BO performance**. In fact, only 20-50 perform best for MolFormer, showing that **pretrained embeddings may allow fewer warmup samples** - a common scenario in real-world, low-data BO. Overall, pretrained embeddings are more efficient for optimization in chemical space (right).

### Check out our youtube video:
[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/4gPTMaarQt0/0.jpg)](https://www.youtube.com/watch?v=4gPTMaarQt0)

## 3) Setup and installation

The code in this repo has been tested on a Linux machine running Python 3.8.8

Run the following terminal commands 

1. Clone repo to local directory

```bash
  git clone https://github.com/eltonpan/bayes-warmup.git
```

2. Set up and activate conda environment
```bash
  cd bayes-warmup
```
```bash
  conda create -n bayes-warmup
```
```bash
  conda activate bayes-warmup
```
```bash
  pip install -r requirements.txt
```

3. Add conda environment to Jupyter notebook

```bash
  conda install -c anaconda ipykernel
```
```bash
  python -m ipykernel install --user --name=bayes-warmup
```

make sure the `bayes-warmup` is the environment under dropdown menu `Kernel` > `Change kernel`

## 3) Code reproducibility

The raw data required to reproduce results in the paper can be found in the `data/` folder. The BO trajectories are saved in the `saving/` folder. Results are visualized in [`bo_trajectory_result_analysis.ipynb`](bo_trajectory_result_analysis.ipynb) (trajectories) and [`visualize_pca.ipynb`](visualize_pca.ipynb) (PCA plot).

1) Get the molecular representations (Morgan fingerprint + MolFormer embeddings) using either:

- Download [`qm9_ECFP6.csv`](https://www.dropbox.com/scl/fi/xnr7cnaonkomt92lb6nuk/qm9_ECFP6.csv?rlkey=l2ou3gl3tev73a720736hwmwq&dl=0) and [`qm9_molformer.csv`](https://www.dropbox.com/scl/fi/ta37h6444c7akzijw8fuj/qm9_molformer.csv?rlkey=9qy8emhs2tjatxaxf4ew59xti&dl=0) place these 2 files in the `data/` folder (highly encouraged)
- **OR** run [`get_ecfp.py`](get_ecfp.py) and [`get_embeddings.py`](get_embeddings.py) (sub-optimal, takes very long, ~9 hours).

2) (Optional) Get the warm-up datasets

- Run [`get_morgan_splits.py`](get_morgan_splits.py) and [`get_molformer_splits.py`](get_molformer_splits.py). This step is optional since `data/` folder already has the warm-up datasets pre-computed.

3) Run the BO experiments using [`run_training.py`](run_training.py)

- **Example 1:** if you would like to run `random` sampling with `morgan` fingerprints, run:

```
python run_training.py --save_path ./saving/morgan/random --data_path ./data/morgan/splits/random/ --test_path ./data/qm9_ECFP6.csv
```

- **Example 2:** if you would like to run `stratified` sampling with `molformer` embedddings, run:

```
python run_training.py --save_path ./saving/molformer/stratified --data_path ./data/molformer/splits/stratified/ --test_path ./data/qm9_molformer.csv
```

The above 2 commands will store trajectories in the `saving/` folder.

4) Visualize results using [`bo_trajectory_result_analysis.ipynb`](bo_trajectory_result_analysis.ipynb) (trajectories) and [`visualize_pca.ipynb`](visualize_pca.ipynb) (PCA plot).


### Repo directory
```
├── all_combi_trajs.pkl: pickle file of all saved trajectories (objective values vs. iteration)
├── bo_trajectory_result_analysis.ipynb: generate trajectory plots
├── data
│   ├── molformer: splits using molformer embeddings
│   ├── morgan: splits using morgan fingerprints
│   └── qm9.csv: QM9 dataset
├── featurizers
│   ├── morgan.py: ECFP6 class
├── figures
│   ├── bo_poster.png
│   ├── bo_results.png
│   ├── bo_trajectory.gif
│   └── stratified.png
├── get_ecfp.py: get morgan fingerprints of molecules
├── get_molformer_embeddings.py: get molformer embeddings of molecules
├── get_molformer_splits.py: get splits based on molformer embeddings
├── get_morgan_splits.py: get splits based on morgan fingerprints
├── kmeans.py: functions for k-means
├── README.md
├── run_training.py: run bayesian optimization of band gaps
├── saving
│   ├── molformer: raw trajectories (best objective so far and molecules) for molformer
│   └── morgan: (best objective so far and molecules) for morgan
├── visualize_pca.ipynb: visualize BO in PCA space, generate gif
└── visualize.py: helper functions for visualizations
```


## 4) Contact
If you have any questions, please free free to contact us at [eltonpan@mit.edu](mailto:eltonpan@mit.edu), [pengfeic@mit.edu](mailto:pengfeic@mit.edu), [jruza@mit.edu](mailto:jruza@mit.edu)
