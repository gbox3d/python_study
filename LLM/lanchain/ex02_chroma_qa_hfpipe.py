#%%
import os
import time
from operator import itemgetter

from transformers import AutoTokenizer, pipeline
from langchain.llms import HuggingFacePipeline

from langchain.vectorstores import Chroma

from langchain import VectorDBQA
from langchain.chains import RetrievalQA

from langchain.embeddings.openai import OpenAIEmbeddings


from langchain import OpenAI

from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnableLambda, RunnablePassthrough
import torch
import pinecone
from dotenv import load_dotenv

# .env 파일 로드 및 Pinecone 초기화
load_dotenv()

#%% Hugging Face 모델 및 파이프라인 로드
model_name = os.getenv("HUGGINGFACE_MODEL")
max_length = int(os.getenv("MAX_LENGTH"))
print(f'Start loading {model_name}')

start_tick = time.time()

tokenizer = AutoTokenizer.from_pretrained(model_name)

hf_pipeline = pipeline(
    task="text-generation", 
    model=model_name, 
    tokenizer=tokenizer,
    # torch_dtype=torch.float16,
    max_length=4096, 
    temperature=0.0,
    do_sample=False,
    device_map="auto" # GPU 상황에 맞게 자동으로 설정
    # device_map="cuda:0"  # GPU 0사용 설정
)

print(f'Load time: {time.time() - start_tick}')

# HuggingFacePipeline 인스턴스 생성
llm = HuggingFacePipeline(
    pipeline=hf_pipeline
    )

# Pinecone 벡터 스토어 설정
embeddings = OpenAIEmbeddings()

# 저장된 벡터 저장소 로드
vector_store = Chroma(
    persist_directory='./stores/chroma_store',
    embedding_function=embeddings
                      )
# retriever = vector_store.as_retriever()
# retriever = vector_store.as_retriever(search_kwargs={"k": 1})
#%% QA chain 생성 
qa_chain = VectorDBQA.from_chain_type(
        llm=llm, 
        chain_type="stuff", 
        vectorstore=vector_store, 
        return_source_documents=True,
        k=1
    )
# qa_chain = RetrievalQA.from_chain_type(llm=llm,
#     chain_type="stuff",
#     retriever=retriever,
#     # chain_type_kwargs=chain_type_kwargs,
#     return_source_documents=True)

#%%
start_tick = time.time()
query = "정읍사 대해서 알려줘"
result = qa_chain({"query": query})
print(f'Query time: {time.time() - start_tick}')

# %%
print(f'question: {result["query"]}')
print(f'answer: {result["result"]}')
print(f'document count : {len(result["source_documents"])}')
# %%
for doc in result['source_documents']:
    print(doc)
# %%
