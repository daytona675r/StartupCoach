# This script embeds and stores documents in a Chroma vector database.
from contentLoader import load_yc_articles, load_ihk_pdfs
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv

#environment variables
load_dotenv()

# Optional: Set path for persistence
PERSIST_DIR = "vector_db"

# 1. Load all content
yc_docs = load_yc_articles()
ihk_docs = load_ihk_pdfs()

# 2. Split all documents
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = splitter.split_documents(yc_docs + ihk_docs)

# 3. Embed documents
embedding_function = OpenAIEmbeddings()

# 4. Create / load Chroma vector DB
vectorstore = Chroma.from_documents(documents=docs, embedding=embedding_function, persist_directory=PERSIST_DIR)

# 5. Save the index
vectorstore.persist()

print(f"✅ Embedded and stored {len(docs)} chunks into ChromaDB.")
