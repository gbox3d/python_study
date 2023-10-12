#%%
from transformers import AutoTokenizer, AutoModelForCausalLM
import transformers
import torch

import yaml

#%%
#load config.yaml
with open('config.yaml', 'r') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
    print(config)
auth_token = config['auth_token']
model_name = config['model_name']

#%%
tokenizer = AutoTokenizer.from_pretrained(model_name,token=auth_token)
pipeline = transformers.pipeline(
    "text-generation",
    model=model_name,
    torch_dtype=torch.float16,
    device_map="auto",
)

def gen(x, max_length=200):
    sequences = pipeline(
        x,
        do_sample=True,
        top_k=10,
        num_return_sequences=1,
        eos_token_id=tokenizer.eos_token_id,
        max_length=max_length,
    )
    return sequences[0]["generated_text"].replace(x, "")

#%%
print(gen("Hello, how are you?"))
# %%
print(gen('전주시에 대해 알려줘'),500)
# %%
print(gen("대한민국에서 유명한 인공지능 유튜버 3명만 나열해봐.", 500))
# %%
print(gen("페미니즘에 대해 한글로 설명해줘", 500))

# %%
