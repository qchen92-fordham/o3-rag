from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings

# Optional Pinecone integration; fall back gracefully when not installed
try:
    from langchain_pinecone import Pinecone, PineconeVectorStore
    PINECONE_AVAILABLE = True
except Exception:
    Pinecone = None
    PineconeVectorStore = None
    PINECONE_AVAILABLE = False

embeddings = OpenAIEmbeddings()
_vectorstore = None


def create_vectorstore(use_pinecone: bool = False):
    """Create and cache a vectorstore. If use_pinecone=True and Pinecone is available,
    use Pinecone; otherwise use an in-memory vector store."""
    global _vectorstore

    loader = [
        TextLoader("data/locations.txt"),
        TextLoader("data/faq.txt"),
        TextLoader("data/insurance-info.txt"),
        TextLoader("data/locations.txt"),
        TextLoader("data/tech-specs.txt"),
        TextLoader("data/terms-of-use.txt"),
    ]

    documents = []
    for ld in loader:
        documents.extend(ld.load())

    # you can also use DirectoryLoader to load all txt files in a directory
    # loader = DirectoryLoader("data/", glob="*.txt")

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    chunks = text_splitter.split_documents(documents)

    if use_pinecone and PINECONE_AVAILABLE:
        # create / populate Pinecone index (requires Pinecone credentials)
        Pinecone.from_documents(chunks, embeddings, index_name="bike-berlin-demo")
        _vectorstore = PineconeVectorStore(index_name="bike-berlin-demo", embedding=embeddings)
    else:
        # fallback to an in-memory vector store (works without external services)
        _vectorstore = InMemoryVectorStore.from_documents(chunks, embeddings)

    return _vectorstore


def search_in_vectorstore(query, use_pinecone: bool = False):
    """Search the cached vectorstore; create it lazily if needed."""
    global _vectorstore
    if _vectorstore is None:
        create_vectorstore(use_pinecone=use_pinecone)

    docs = _vectorstore.similarity_search(query, k=1)
    return docs[0].page_content
