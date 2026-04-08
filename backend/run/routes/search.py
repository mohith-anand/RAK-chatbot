from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from run.services.product_search_service import search_tiles
from run.services.gemini_service import generate_tile_response
from run.services.recommendation_engine import extract_tile_preferences
router = APIRouter()

class SearchRequest(BaseModel):
    query: str
    history: list = []
    n_results: int = 5

@router.post("/search")
def search_products(request: SearchRequest):
    try:
        preferences = extract_tile_preferences(request.query)
        
        # 1. Execute the vector search and re-ranking
        results = search_tiles(
            user_query=request.query,
            n_results=request.n_results
        )

        # 2. Generate the AI sales assistant response using Gemini 2.5 Flash
        ai_response = generate_tile_response(
            user_query=request.query,
            tile_results=results,
            history=request.history
        )

        # 3. Return the combined data
        return {
            "query": request.query,
            "preferences": preferences,
            "count": len(results),
            "ai_response": ai_response,
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")