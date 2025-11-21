import json
import chromadb
from chromadb.utils import embedding_functions
import os
import glob

def ingest_data():
    # Initialize ChromaDB client (persistent)
    client = chromadb.PersistentClient(path="./chroma_db")
    
    # Use default embedding function (all-MiniLM-L6-v2)
    sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    
    # Create or get collection
    collection = client.get_or_create_collection(
        name="cyber_knowledge_base",
        embedding_function=sentence_transformer_ef
    )
    
    # Load all JSON files (output.json, output_japan.json, output_nyc.json)
    json_files = glob.glob("output*.json")
    
    if not json_files:
        print("No output JSON files found. Run the crawlers first.")
        return

    all_data = []
    for json_file in json_files:
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                if data:
                    all_data.extend(data)
                    print(f"Loaded {len(data)} items from {json_file}")
        except FileNotFoundError:
            print(f"{json_file} not found, skipping.")
        except json.JSONDecodeError:
            print(f"Error decoding {json_file}, skipping.")

    if not all_data:
        print("No data to ingest.")
        return

    print(f"\nIngesting {len(all_data)} total items...")
    
    ids = []
    documents = []
    metadatas = []
    
    for i, item in enumerate(all_data):
        # Create a unique ID with region prefix
        doc_id = f"{item['region']}_{i}"
        
        # Prepare metadata
        meta = {
            "region": item["region"],
            "source_url": item["source_url"],
            "title": item["title"],
            "published_date": item["published_date"] or "",
            "scraped_at": item["scraped_at"]
        }
        
        # Prepare document text (Title + Content)
        text = f"{item['title']}\n\n{item['content_block']}"
        
        ids.append(doc_id)
        documents.append(text)
        metadatas.append(meta)

    # Add to collection
    collection.upsert(
        ids=ids,
        documents=documents,
        metadatas=metadatas
    )
    
    print(f"Successfully ingested {len(ids)} documents into ChromaDB.")
    
    # Print region breakdown
    regions = {}
    for meta in metadatas:
        region = meta['region']
        regions[region] = regions.get(region, 0) + 1
    
    print("\nRegion breakdown:")
    for region, count in sorted(regions.items()):
        print(f"  {region}: {count} documents")

if __name__ == "__main__":
    ingest_data()
