from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import Pinecone, PineconeVectorStore


embeddings = OpenAIEmbeddings()

def create_vectorstore():
    loader = [
    TextLoader("data/locations.txt"),
    TextLoader("data/faq.txt"),
    TextLoader("data/insurance-info.txt"),
    TextLoader("data/locations.txt"),
    TextLoader("data/tech-specs.txt"),
    TextLoader("data/terms-of-use.txt"),
    ]

    documents = []
    for loader in loader:
        documents.extend(loader.load())

    # you can also use DirectoryLoader to load all txt files in a directory
    #loader = DirectoryLoader("data/", glob="*.txt")

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)

    chunks = text_splitter.split_documents(documents)

    # Example1: Using InMemoryVectorStore
    #vectorstore = InMemoryVectorStore.from_documents(chunks, embeddings)

    # Example2: Using Pinecone VectorStore
    Pinecone.from_documents(chunks, embeddings, index_name="bike-berlin-demo")
    


def search_in_vectorstore(query):
    #query = "Where is the closest bike station? I live in Berlin Alexanderplatz."
    vectorstore = PineconeVectorStore(index_name="bike-berlin-demo", embedding=embeddings)
    docs = vectorstore.similarity_search(query, k=1)
    return docs[0].page_content
