from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

#environment variables
load_dotenv()

# Setup
PERSIST_DIR = "vector_db"
embedding_function = OpenAIEmbeddings()

# Load existing Chroma DB
vectorstore = Chroma(persist_directory=PERSIST_DIR, embedding_function=embedding_function)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# Define test queries
test_queries = [
    "What are the steps to start a startup?", #Expected: Content from Y Combinator or IHK that outlines early-stage startup phases, MVPs, etc.
    "What business forms are available when starting in Germany?", #Expected: Content from IHK PDFs describing sole proprietorship, GmbH, UG, etc.
    "How do startups in space tech get funding?" #Expected: Should return either:Generic startup funding advice (from YC or IHK),Or nothing relevant — a good check to see if your fallback handling is needed.
]

# Run test queries and display results
for query in test_queries:
    print(f"\n🔍 Query: {query}")
    results = retriever.invoke(query)
    if not results:
        print("❌ No results found.")
    for i, doc in enumerate(results, 1):
        print(f"\nResult {i}:")
        print(doc.page_content[:500])  # Preview first 500 characters
        print("Source:", doc.metadata.get("source", "unknown"))
