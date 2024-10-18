from langchain_community.document_loaders import TextLoader


from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

ctfcollection_name="ctf-chroma"

def get_retriever(paths):

    docs = [TextLoader(path).load() for path in paths]
    docs_list = [item for sublist in docs for item in sublist]

    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=250, chunk_overlap=0
    )
    doc_splits = text_splitter.split_documents(docs_list)

    # Add to vectorDB
    embedings=OpenAIEmbeddings(model="text-embedding-v3" ,base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")

    # vector = embedings.client.create(
    #     model="text-embedding-v1",
    #     input=['风急天高猿啸哀', '渚清沙白鸟飞回', '无边落木萧萧下', '不尽长江滚滚来'],
    #     encoding_format="float"
    #     )
    # print(vector.model_dump_json())

    from langchain_core.embeddings import FakeEmbeddings
    vectorstore = Chroma.from_documents(
        documents=doc_splits,
        collection_name=ctfcollection_name,
        embedding=FakeEmbeddings(size=100),
    )




    retriever = vectorstore.as_retriever()
    return retriever