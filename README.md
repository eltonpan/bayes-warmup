# AC BO Hackathon 2024: Team `bayes-warmup`

This is the official repository of the project 27:

**How does initial warm-up data influence Bayesian optimization in low-data experimental settingss**  (AC BO Hackathon 2024)

Elton Pan (MIT), Jurgis Ruza (MIT), Pengfei Cai (MIT)

<p align="center">
  <img src="/figures/bo_trajectory.gif" width="400"/> 
</p>

## 1) Overview

Real-world experiments in chemistry and materials science often involve very small initial datasets (10-100 data points). In this project, we propose to investigate how the 1) size and 2) distribution of the initial dataset influence the performance of bayesian optimization algorithms. We propose experiments on molecular property optimization tasks.

## 2) Approach and main findings

<p align="center">
<img src="/figures/stratified.png" width="350"/> 
</p>

### A) Stratified sampling is more efficient than random
We show that stratified sampling as a more efficient way to sample a warmup dataset. First, a k-means clustering algorithm determines the centroids (green), resulting in clusters shown above. Stratified sampling (i.e. sampling same number of datapoints per cluster) is then performed.


<p align="center">
  <img src="/figures/bo_poster.png" width="700"/> 
</p>

### B) Pretrained embeddings allow more more efficient exploration in low-data regimes
Here, we vary the number of datapoints from 5-200. We show that simple representations such as Morgan fingerprints (bottom left), more warmup samples improves BO performance. However, this is not true for pretrained embeddings such as MolFormer (bottom center), where more warmup datapoints do not necessarily improve BO performance. In fact, only 20-50 perform best for MolFormer, showing that pretrained embeddings may allow fewer warmup samples - a scenario common in real-world BO. Overall, pretrained embeddings are more efficient for optimization in chemical space (bottom right).






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
  conda env create -f env/env.yml
```
```bash
  conda activate bayes-warmup
```

3. Add conda environment to Jupyter notebook
```bash
  conda install -c anaconda ipykernel
```
```bash
  python -m ipykernel install --user --name=bayes-warmup
```

4. Open jupyter notebooks
```bash
  jupyter notebook <notebook_name>.ipynb
```

make sure the `bayes-warmup` is the environment under dropdown menu `Kernel` > `Change kernel`

## 3) Code reproducibility

The data required to reproduce results in the paper can be found in `datasets/` directory:
```
├── analysis.ipynb
├── data
│   ├── molformer
│   │   └── splits
│   │   │   ├── fragment
│   │   │   ├── random
│   │   │   └── stratified
│   ├── morgan
│   │   ├── qm9_ECFP6.csv
│   │   └── splits
│   │       ├── fragment
│   │       ├── random
│   │       └── stratified
│   └── qm9.csv
├── featurizers
│   ├── morgan.py
│   └── __pycache__
│       └── morgan.cpython-37.pyc
├── figures
├── get_ecfp.py
├── kmeans.py
├── nohup.out
├── __pycache__
│   └── kmeans.cpython-37.pyc
├── README.md
└── run_training.py
```