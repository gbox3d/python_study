#%%
import os
from transformers import AutoModelForCausalLM, AutoTokenizer
from langchain.llms import HuggingFaceHub
from langchain.vectorstores import Pinecone
from langchain import VectorDBQA
from langchain.embeddings.openai import OpenAIEmbeddings

import pinecone
from dotenv import load_dotenv

import time

# .env 파일 로드
load_dotenv()

pinecone.init(
    api_key=os.getenv("PINECONE_API_KEY"),
    environment=os.getenv("PINECONE_ENVIRONMENT"),
)

#%%

start_tick = time.time()
# Hugging Face 모델과 토크나이저 로드
model_name = "meta-llama/Llama-2-7b-chat-hf"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

print(f'load time: {time.time() - start_tick}')

#%%
# Langchain에 모델 통합
# HuggingFaceHub 인스턴스 생성
hf_hub = HuggingFaceHub(
    repo_id=model_name,
    # huggingfacehub_api_token='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',
    task="text-generation"  # 적절한 task를 선택하세요.
)

#%%
# Pinecone 벡터 스토어 설정
# 여기서는 기존 Pinecone 설정을 사용합니다.
embeddings = OpenAIEmbeddings()
pinecone_client = Pinecone.from_existing_index(
    embedding=embeddings,
    index_name = os.getenv("PINECONE_INDEX_NAME")
    )

#%%
# VectorDBQA 구성

qa = VectorDBQA.from_chain_type(
        llm=hf_hub, 
        chain_type="stuff", 
        vectorstore=pinecone_client, 
        return_source_documents=True
    )

# 쿼리 실행
query = "What is a vector DB? Give me a 15 word answer for a beginner"
result = qa({"query": query})
print(result)

# %%
