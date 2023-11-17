#%%
import os
import time
from operator import itemgetter

from transformers import AutoTokenizer, pipeline
from langchain.llms import HuggingFacePipeline

from dotenv import load_dotenv
# .env 파일 로드 및 Pinecone 초기화
load_dotenv()

#%% Hugging Face 모델 및 파이프라인 로드
model_name = os.getenv("HUGGINGFACE_MODEL")
print(f'Start loading {model_name}')

start_tick = time.time()

tokenizer = AutoTokenizer.from_pretrained(model_name)

hf_pipeline = pipeline(
    "text-generation", 
    model=model_name, 
    tokenizer=tokenizer,
    max_length=1000,
    device_map="auto"  # GPU 사용 설정
)

print(f'Load time: {time.time() - start_tick}')

# HuggingFacePipeline 인스턴스 생성
llm = HuggingFacePipeline(pipeline=hf_pipeline)
print(llm)
# %%
start_tick = time.time()
query = "페미니즘에 대해 한글로 설명해줘"
# 질문에 대한 응답 생성
response = llm.invoke(query)
print(response)
print(f'Inference time: {time.time() - start_tick}')

# %%
from langchain.prompts import PromptTemplate

prompt = PromptTemplate.from_template("What is a good name for a company that makes {product}?")
prompt.format(product="colorful socks")

# %%
