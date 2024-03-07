from langchain_community.embeddings import LlamaCppEmbeddings
from langchain_community.llms import GPT4All
from langchain.vectorstores.faiss import FAISS
from langchain.chains import ConversationalRetrievalChain
import torch

class HSU:
    def rag(question):
        model_path = "../LLM/Models/mistral-7b-openorca.Q4_0.gguf"
        index_path = "../LLM/HSU_index"
        
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {device}")
        
        embeddings = LlamaCppEmbeddings(model_path=model_path)
        index = FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)
        llm = GPT4All(model=model_path, device=device)
        
        qa = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=index.as_retriever(),
            chain_type="stuff",
            verbose=True,
            max_tokens_limit=1000,
        )
        
        # Chatbot loop
        chat_history = []
        result = qa({"question": question, "chat_history": chat_history})
        return result