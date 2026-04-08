import os
import google.generativeai as genai
import chromadb
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# --- PATH CONFIGURATION ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.dirname(BASE_DIR)
CHROMA_PATH = os.path.join(BACKEND_DIR, "data", "vector_db")
EMBEDDING_MODEL = "models/gemini-embedding-2-preview"

# Initialize ChromaDB Client
client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = client.get_collection("rak_tiles_products")

def search_products(user_query: str, n_results: int = 3):
    query_lower = user_query.lower()
    
    # 1. Generate Query Embedding
    formatted_query = f"task: retrieval_query | {user_query}"
    result = genai.embed_content(
        model=EMBEDDING_MODEL, 
        content=formatted_query, 
        task_type="retrieval_query"
    )
    
    # Handle API response variations
    query_embedding = result["embedding"] if "embedding" in result else result["embeddings"][0]

    # 2. Initial Vector Search (Fetch 25 candidates for re-ranking)
    raw_results = collection.query(query_embeddings=[query_embedding], n_results=25)

    processed_list = []
    
    # 3. Pre-extract Size (e.g., '60x60', '80x80') using Regex
    size_match = re.search(r'(\d{2,3}x\d{2,3})', query_lower)
    target_size = size_match.group(1) if size_match else None

    # 4. Re-ranking Loop
    for i in range(len(raw_results["ids"][0])):
        metadata = raw_results["metadatas"][0][i]
        dist = raw_results["distances"][0][i]
        base_similarity = round(1 - dist, 4)
        
        final_score = base_similarity

        # --- RULE 1: SURFACE FINISH (PRIORITY FILTER) ---
        surface = metadata.get("surface", "").lower()
        polished_query = any(word in query_lower for word in ["polished", "gloss", "shiny", "reflective", "high gloss"])
        matt_query = any(word in query_lower for word in ["matt", "matte", "natural"])

        if polished_query:
            if "polished" in surface: final_score += 0.60
            else: final_score -= 0.40 # Penalize wrong finish
        
        if matt_query:
            if "matt" in surface: final_score += 0.40
            else: final_score -= 0.30

        # --- RULE 2: COLOR & SYNONYMS ---
        color = metadata.get("color", "").lower()
        if "white" in query_lower or "off-white" in query_lower:
            if "white" in color: final_score += 0.35
            elif "ivory" in color or "beige" in color: final_score += 0.15 # Synonym Match
        elif "grey" in query_lower or "gray" in query_lower:
            if "grey" in color or "anthracite" in color: final_score += 0.35
        elif color in query_lower and len(color) > 2:
            final_score += 0.30

        # --- RULE 3: SIZE MATCHING ---
        tile_size = metadata.get("size_cm", "")
        if target_size and target_size in tile_size:
            final_score += 0.50 # Size is a major factor

        # --- RULE 4: OUTDOOR / TECHNICAL ---
        suitable = metadata.get("suitable_for", "").lower()
        application = metadata.get("application", "").lower()
        outdoor_query = any(word in query_lower for word in ["outdoor", "exterior", "patio", "garden"])
        
        if outdoor_query:
            if "outdoor" in suitable or "outdoor" in application:
                final_score += 0.65
            else:
                final_score -= 0.50 # Penalize indoor tiles for outdoor searches

        # Store in list for sorting
        processed_list.append({
            "series": metadata.get("series_name", "Unknown"),
            "color": metadata.get("color", "N/A"),
            "surface": metadata.get("surface", "N/A"),
            "size": metadata.get("size_cm", "N/A"),
            "sku": raw_results["ids"][0][i],
            "image_path": metadata.get("image_path", "N/A"),
            "app": application,
            "suitable": suitable,
            "base_score": base_similarity,
            "final_score": round(final_score, 4)
        })

    # 5. Final Sort and Slice
    sorted_results = sorted(processed_list, key=lambda x: x["final_score"], reverse=True)
    return sorted_results[:n_results]

if __name__ == "__main__":
    print("\n" + "="*60)
    print(" RAK CERAMICS - INTELLIGENT SEARCH ENGINE")
    print("="*60)
    
    while True:
        query = input("\nCustomer Query (or 'exit'): ")
        if query.lower() in ['exit', 'quit']: break
        
        # We retrieve the top 3 results
        top_3 = search_products(query, n_results=3)
        
        if not top_3:
            print("No matching tiles found.")
            continue

        for i, tile in enumerate(top_3):
            print(f"\n[{i+1}] {tile['series'].upper()} | SKU: {tile['sku']}")
            print(f"    Color: {tile['color']} | Finish: {tile['surface']} | Size: {tile['size']}")
            print(f"    Image: {tile['image_path']}")
            print(f"    Application: {tile['app']}")
            print(f"    Suitable For: {tile['suitable']}")
            print(f"    Rank Score: [AI Base: {tile['base_score']}] -> [Final: {tile['final_score']}]")
            print("-" * 60)