from langchain_community.document_loaders import PlaywrightURLLoader, PyPDFLoader
from bs4 import BeautifulSoup, SoupStrainer
import os

# Define article URLs
YC_ARTICLE_URLS = [
    "https://www.ycombinator.com/library/4A-a-guide-to-seed-fundraising",
    "https://www.ycombinator.com/library/Ek-stages-of-startups",
    "https://www.ycombinator.com/library/8g-how-to-get-startup-ideas",
    "https://www.ycombinator.com/library/61-startup-growth",
    "https://www.ycombinator.com/library/61-order-of-operations-for-starting-a-startup",
    "https://www.ycombinator.com/library/8y-before-the-startup",
    "https://www.ycombinator.com/library/4D-do-things-that-don-t-scale",
    "https://www.ycombinator.com/library/6t-how-to-succeed-with-a-startup",
    "https://www.ycombinator.com/library/En-what-is-a-startup",
    "https://www.ycombinator.com/library/carousel/Essays%20by%20Paul%20Graham",
    "https://www.ihk.de/berlin/english/en/s-987416/finanzierung/mb-gruenderzuschuss-eng-4342572"
]

# Define knowledge base raw path
RAW_PDF_DIR = "knowledgebase/raw"

# Load all PDF files in the folder
def load_ihk_pdfs():
    pdf_files = [f for f in os.listdir(RAW_PDF_DIR) if f.endswith(".pdf")]
    documents = []
    for filename in pdf_files:
        filepath = os.path.join(RAW_PDF_DIR, filename)
        loader = PyPDFLoader(filepath)
        docs = loader.load()
        documents.extend(docs)
    return documents


# Load yc rendered content with Playwright
def load_yc_articles():
    loader = PlaywrightURLLoader(urls=YC_ARTICLE_URLS, remove_selectors=["header", "footer", "nav"])
    documents = loader.load()
    return documents

# Example usage:
#raw_docs = load_ihk_pdfs()
# docs = load_yc_articles()
#for doc in raw_docs:
#     print(f"Title: {doc.metadata.get('title', 'No title')}")
#     print(f"URL: {doc.metadata.get('source', 'No source')}")
#     print(f"Content length: {len(doc.page_content)} characters\n")
#     print(doc.page_content[:500])
# Now pass docs to RecursiveCharacterTextSplitter for chunking
