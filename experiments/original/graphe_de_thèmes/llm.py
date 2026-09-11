from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI

# Load documents
loader = TextLoader("../web_scraping/s2a_thèses_with_pdf.txt")  # Or use multiple files
documents = loader.load()
embedding = OpenAIEmbeddings(openai_api_key="your-api-key-here")
llm = ChatOpenAI(openai_api_key="your-api-key-here")

# Split documents into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
docs = text_splitter.split_documents(documents)

# Embed and store in Chroma vector store
embedding = OpenAIEmbeddings()
db = Chroma.from_documents(docs, embedding)

# Set up retriever
retriever = db.as_retriever()

# Load model
llm = ChatOpenAI(model_name="gpt-3.5-turbo")  # or "gpt-4"

# QA chain
qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

# Ask a question
query = "What is the main topic of these documents?"
result = qa.run(query)

print(result)
