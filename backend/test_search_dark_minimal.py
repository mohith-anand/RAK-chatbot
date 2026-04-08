from run.services.product_search_service import search_tiles

def test_dark_minimal_search():
    query = "Minimal look tiles for Commercial Space and Dark color"
    results = search_tiles(query, n_results=10)
    
    print(f"\nSearch Query: '{query}'")
    print("-" * 50)
    
    found_lounge = False
    for i, res in enumerate(results):
        is_lounge = "lounge" in res['series_name'].lower()
        is_dark = any(c in res['color'].lower() for c in ["black", "dark", "anthracite", "charcoal"])
        status = "✅ LOUNGE DARK" if (is_lounge and is_dark) else "❌ OTHER"
        if is_lounge and is_dark: found_lounge = True
        
        print(f"[{i+1}] {res['series_name']} ({res['category']}) - {res['color']} - {status}")
        print(f"    Scores: AI: {res['base_score']} | Final: {res['final_score']}")

    if not found_lounge:
        print("\nFAIL: No Lounge Black/Dark tiles found in top 10 results!")
    else:
        print("\nSUCCESS: Found Lounge Dark tiles.")

if __name__ == "__main__":
    test_dark_minimal_search()
