from langchain_community.document_loaders import TextLoader
import os

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings

ctfcollection_name="ctf-chroma"

embeddings=DashScopeEmbeddings(dashscope_api_key=os.environ.get("OPENAI_API_KEY"),model="text-embedding-v3" )

vectorstore = Chroma(
        collection_name=ctfcollection_name,
        embedding_function=embeddings,
        persist_directory="./chroma_langchain_qwen_db",
    )

def save_vector(paths):

    docs = [TextLoader(path).load() for path in paths]
    docs_list = [item for sublist in docs for item in sublist]

    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=250, chunk_overlap=0
    )
    doc_splits = text_splitter.split_documents(docs_list)

    # Add to vectorDB


    vectorstore.add_documents(documents=doc_splits)

    return vectorstore