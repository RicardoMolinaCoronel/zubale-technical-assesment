from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from typing import List
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()
class RetrieverAgent:
    def __init__(self, index_path: str = None):
        model_name = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
        self.k = int(os.getenv("TOP_K", 1))
        self.embedder = HuggingFaceEmbeddings(model_name=model_name)

        if index_path and Path(index_path).exists():
            self.vectorstore = FAISS.load_local(index_path, self.embedder)
        else:
            self.index_documents_from_folder("documents")

    def index_documents_from_folder(self, folder_path: str):
        base_dir = Path(__file__).resolve().parent.parent  # sube a raíz del proyecto
        folder = base_dir / folder_path
        if not folder.exists() or not folder.is_dir():
            raise FileNotFoundError(f"Folder not found: {folder_path}")

        texts = []
        for file in folder.glob("*.txt"):
            with open(file, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:
                    texts.append(content)
        if not texts:
            raise ValueError(f"No valid .txt files with content found in {folder_path}")

        self.vectorstore = FAISS.from_texts(texts, self.embedder)

    def retrieve(self, query: str) -> List[Document]:
        if not self.vectorstore:
            raise ValueError("Vectorstore not initialized. Index documents first.")
        return self.vectorstore.similarity_search(query, k=self.k)

    def __call__(self, state):
        query = state["query"]
        docs = self.retrieve(query)
        return {"query": query, "docs": docs}
