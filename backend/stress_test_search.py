import time
from run.services.product_search_service import search_tiles

TEST_CASES = [
    {
        "query": "what marble collections do you have?",
        "expected_category": "marble"
    },
    {
        "query": "show me some concrete effect tiles for floor",
        "expected_category": "concrete"
    },
    {
        "query": "do you have any wood look tiles?",
        "expected_category": "wood"
    },
    {
        "query": "metallic wall tiles for modern kitchen",
        "expected_category": "metal"
    },
    {
        "query": "best tiles for outdoor patio",
        "expected_suitable": "outdoor"
    },
    {
        "query": "polished white tiles 60x120",
        "expected_color": "white",
        "expected_surface": "polished"
    },
    {
        "query": "heavy commercial flooring for a mall",
        "expected_suitable": "heavy commercial"
    },
    {
        "query": "grey stone tiles 60x60",
        "expected_category": "stone",
        "expected_color": "grey"
    },
    {
        "query": "tiles from the Calacatta Africa series",
        "expected_series": "calacatta africa"
    },
    {
        "query": "resin look tiles for living room",
        "expected_category": "resin"
    }
]

def run_stress_test():
    print("\n" + "="*80)
    print(" RAK CERAMICS - AI SEARCH STRESS TEST (10 QUESTIONS)")
    print("="*80)
    
    passed = 0
    total = len(TEST_CASES)
    
    for i, test in enumerate(TEST_CASES):
        print(f"\n[{i+1}/{total}] Query: '{test['query']}'")
        
        start_time = time.time()
        results = search_tiles(test['query'], n_results=3)
        duration = time.time() - start_time
        
        print(f"      Time taken: {duration:.2f}s")
        
        if not results:
            print("      ❌ FAILED: No results found.")
            continue
            
        # Check top result
        top_res = results[0]
        meta_str = f"Cat: {top_res['category']} | Series: {top_res['series_name']} | Color: {top_res['color']} | Suitable: {top_res['suitable_for']}"
        print(f"      Top Result: {top_res['series_name'].upper()} ({meta_str})")
        print(f"      Score: {top_res['final_score']}")
        
        # Validation Logic
        is_valid = True
        reasons = []
        
        if "expected_category" in test:
            if test['expected_category'].lower() not in top_res['category'].lower():
                is_valid = False
                reasons.append(f"Category mismatch (Expected {test['expected_category']})")
        
        if "expected_suitable" in test:
            if test['expected_suitable'].lower() not in top_res['suitable_for'].lower():
                is_valid = False
                reasons.append(f"Suitability mismatch (Expected {test['expected_suitable']})")
                
        if "expected_color" in test:
            if test['expected_color'].lower() not in top_res['color'].lower():
                is_valid = False
                reasons.append(f"Color mismatch (Expected {test['expected_color']})")

        if "expected_series" in test:
            if test['expected_series'].lower() not in top_res['series_name'].lower():
                is_valid = False
                reasons.append(f"Series mismatch (Expected {test['expected_series']})")
        
        if is_valid:
            print("      ✅ PASSED")
            passed += 1
        else:
            print(f"      ❌ FAILED: {', '.join(reasons)}")
            
        # Small delay to avoid hitting limits too fast
        time.sleep(1)

    print("\n" + "="*80)
    print(f" TEST SUMMARY: {passed}/{total} Passed")
    print("="*80)

if __name__ == "__main__":
    run_stress_test()
