import chromadb
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHROMA_PATH = os.path.join(BASE_DIR, "data", "vector_db")
client = chromadb.PersistentClient(path=CHROMA_PATH)

try:
    collection = client.get_collection("rak_tiles_products")
    results = collection.get(limit=10)
    print(f"Total products in DB: {collection.count()}")
    print("Metadata for first 10 products:")
    for i, meta in enumerate(results['metadatas']):
        print(f"{i+1}: {meta.get('series_name')} - {meta.get('category')}")
except Exception as e:
    print(f"Error: {e}")
