# AC BO Hackathon 2024: Team `bayes-warmup`

This is the official repository of the project 27:

**How does initial warm-up data influence Bayesian optimization in low-data experimental settingss** by

Elton Pan, Jurgis Ruza, Pengfei Cai

MIT

<p align="center">
  <img src="/figures/stratified.png" width="350"/> 
  <img src="/figures/bo_trajectory.gif" width="400"/> 
</p>

<!-- <p align="center">
  <img src="/figures/bo_trajectory.gif" width="600"/> 
</p> -->



## 1) Overview

Some text



## 2) Setup and installation

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