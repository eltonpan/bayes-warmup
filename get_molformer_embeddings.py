import torch
from transformers import AutoModel, AutoTokenizer
from tqdm import tqdm 
import pandas as pd

# using https://huggingface.co/ibm/MoLFormer-XL-both-10pct pretrained MolFormer

device = "cuda:2"
model = AutoModel.from_pretrained("ibm/MoLFormer-XL-both-10pct", deterministic_eval=True, trust_remote_code=True).to(device)
tokenizer = AutoTokenizer.from_pretrained("ibm/MoLFormer-XL-both-10pct", trust_remote_code=True)

df = pd.read_csv("data/qm9.csv")
smiles_list = df["smiles"].tolist()
gap_list = df["gap"].tolist()
inputs = tokenizer(smiles_list, padding=True, return_tensors="pt").to(device)

all_embeddings = []
batch_size = 4
max_range = len(smiles_list)//batch_size

for i in tqdm(range(0, max_range+1), desc="Processing batches"):
    print(i*batch_size, (i+1)*batch_size)
    batch_input = {'input_ids': inputs["input_ids"][i*batch_size : (i+1)*batch_size], 
                   'attention_mask': inputs["attention_mask"][i*batch_size : (i+1)*batch_size]}
    batch_input = {k: v.to(device) for k, v in batch_input.items()}
    with torch.no_grad():
        outputs = model(**batch_input)
    all_embeddings.append(outputs.pooler_output)

all_embeddings = torch.cat(all_embeddings, dim=0)
embeddings_df = pd.DataFrame(all_embeddings.cpu().numpy(), columns=[f'mf{i}' for i in range(0, 768)])

embeddings_df = embeddings_df.drop(columns=['Unnamed: 0'])
embeddings_df["smiles"] = smiles_list
embeddings_df["gap"] = gap_list
embeddings_df['gap'] = embeddings_df['gap']*27.2114

embeddings_df.to_csv("data/molformer/qm9_molformer.csv")