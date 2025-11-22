import chromadb
from chromadb.utils import embedding_functions
import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

class RAGPipeline:
    def __init__(self):
        self.client = chromadb.PersistentClient(path="./chroma_db")
        # Use the same embedding function as ingestion
        self.ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
        self.collection = self.client.get_collection(name="cyber_knowledge_base", embedding_function=self.ef)
        
        # Initialize Ollama client with environment-configured base URL
        ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        try:
            self.llm = ChatOllama(
                model="llama3.2", 
                temperature=0,
                base_url=ollama_base_url
            )
            print(f"Connected to Ollama at {ollama_base_url}")
        except Exception as e:
            self.llm = None
            print(f"Warning: Failed to connect to Ollama at {ollama_base_url}: {e}")

    def query(self, query_text: str, region: str = None):
        # Query collection with optional region filter
        if region:
            results = self.collection.query(
                query_texts=[query_text],
                n_results=5,
                where={"region": region}
            )
        else:
            results = self.collection.query(
                query_texts=[query_text],
                n_results=5
            )
        
        if not results['documents'] or not results['documents'][0]:
             return "I can only answer using official cybersecurity information from the selected region's government portals. No relevant data was found.", []

        documents = results['documents'][0]
        metadatas = results['metadatas'][0]
        distances = results['distances'][0]
        
        # Filter results by relevance threshold (L2 distance)
        RELEVANCE_THRESHOLD = 1.2
        
        context_parts = []
        sources = []
        
        for i, doc in enumerate(documents):
            distance = distances[i]
            meta = metadatas[i]
            
            # Only include relevant sources
            if distance < RELEVANCE_THRESHOLD:
                # Add source number to context for citation
                source_num = len(sources) + 1
                context_parts.append(f"[Source {source_num}] {meta['title']}\nContent: {doc}")
                sources.append({
                    "title": meta['title'],
                    "url": meta['source_url'],
                    "region": meta['region']
                })
            
        context = "\n\n".join(context_parts)
        
        if not context or len(sources) == 0:
            return "I can only answer using official cybersecurity information from the selected region's government portals. No relevant data was found.", []

        if self.llm:
            # Generate with explicit source citation instruction
            region_context = f" for {region}" if region else " from multiple regions"
            prompt = ChatPromptTemplate.from_template("""
                You are a cybersecurity expert assistant{region_context}. 
                Answer the user's question strictly based on the provided context from official government sources.
                
                IMPORTANT: When you reference information from a source, cite it using the source number in square brackets like [1] or [2].
                For example: "Ransomware is malicious software [1] that encrypts files [2]."
                
                If the answer is not in the context, say "I can only answer using official cybersecurity information from government portals. No relevant data was found."
                
                Context:
                {context}
                
                Question: 
                {question}
                
                Answer (remember to cite sources with [1], [2], etc.):
            """)
            chain = prompt | self.llm
            try:
                response = chain.invoke({"context": context, "question": query_text, "region_context": region_context})
                answer = response.content
            except Exception as e:
                answer = (
                    "**AI Engine Unavailable**\n\n"
                    "Unable to generate summary. Please ensure the Ollama service is running.\n\n"
                    "**Relevant Information:**\n\n"
                    f"{context}"
                )
        else:
            answer = "NOTE: Ollama not available. Showing retrieved context directly:\n\n" + context
            # Truncate if too long for a simple test
            if len(answer) > 2000:
                answer = answer[:2000] + "... (truncated)"

        return answer, sources
