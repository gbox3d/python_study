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

import pinecone
from dotenv import load_dotenv

# .env 파일 로드 및 Pinecone 초기화
load_dotenv()

#%%
llm = OpenAI()
# Pinecone 벡터 스토어 설정
embeddings = OpenAIEmbeddings()

# 저장된 벡터 저장소 로드
vector_store = Chroma(
    persist_directory='./stores/chroma_store',
    embedding_function=embeddings
                      )
retriever = vector_store.as_retriever()
#%% QA 모델 설정
vector_db_qa = VectorDBQA.from_chain_type(
        llm=llm, 
        chain_type="stuff", 
        vectorstore=vector_store, 
        return_source_documents=True,
        k=1
    )

#%%
start_tick = time.time()
query = "정읍사 에 대해서 알려줘"
result = vector_db_qa({"query": query})
print(result)
print(f'Query time: {time.time() - start_tick}')

# %%
print(f'question: {result}')
print(f'answer: {result["result"]}')
print(len(result['source_documents']))
# %%
for doc in result['source_documents']:
    print(doc)
# %%
