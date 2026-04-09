# backend/services/gemini_service.py

import os
import google.generativeai as genai
from dotenv import load_dotenv
from pathlib import Path

dotenv_path = Path(__file__).resolve().parents[2] / '.env'
load_dotenv(dotenv_path)
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError(f"GEMINI_API_KEY not set. Checked: {dotenv_path}")

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.5-flash")


def generate_tile_response(user_query: str, tile_results: list, history: list = []):
    try:
        if not tile_results and not history:
            return "I could not find any matching tiles for that requirement."

        # Format conversation history
        history_text = ""
        if history:
            history_text = "\nPrevious Conversation:\n"
            for msg in history[-10:]: # Last 10 messages for deeper context
                role = "User" if msg.get("role") == "user" else "Assistant"
                history_text += f"{role}: {msg.get('text', '')}\n"

        tile_text = ""
        for idx, tile in enumerate(tile_results, start=1):
            tile_text += f"""
Tile {idx}:
- Series: {tile.get('series_name', 'N/A')}
- Color: {tile.get('color', 'N/A')}
- Finish: {tile.get('surface', 'N/A')}
- Size: {tile.get('size_cm', 'N/A')}
- Application: {tile.get('application', 'N/A')}
- Suitable For: {tile.get('suitable_for', 'N/A')}
- SKU: {tile.get('sku', 'N/A')}
"""

        prompt = f"""
You are a tile recommendation assistant for RAK Ceramics.
{history_text}

Current Customer query:
{user_query}

Matching tiles:
{tile_text}

Return valid JSON only.

Format:
{{
  "ai_summary": "...",
  "recommended_tiles": [
    {{
      "series_name": "...",
      "product_name": "...",
      "color": "...",
      "surface": "...",
      "size_cm": "...",
      "application": "...",
      "suitable_for": "...",
      "sku": "...",
      "why_recommended": "..."
    }}
  ]
}}

Rules:
- Recommend maximum 4 tiles
- Keep summary concise
- why_recommended should be 1 sentence
- Return valid JSON only, no markdown
"""
        
        response = model.generate_content(prompt)
        
        text_response = ""
        if hasattr(response, "text") and response.text:
            text_response = response.text
        elif hasattr(response, "candidates") and response.candidates:
            try:
                text_response = response.candidates[0].content.parts[0].text
            except Exception:
                return {"ai_summary": "I found some tiles but couldn't generate a recommendation summary.", "recommended_tiles": []}

        # Clean markdown if present
        text_response = text_response.replace("```json", "").replace("```", "").strip()
        
        import json
        try:
            return json.loads(text_response)
        except Exception:
            return {
                "ai_summary": text_response if text_response else "I found some matching tiles for you.",
                "recommended_tiles": []
            }

    except Exception as e:
        print("Gemini Error:", str(e))
        return {
            "ai_summary": "I apologize, but I'm having a bit of trouble generating a detailed recommendation right now. However, I have found some tiles below that match your criteria.",
            "recommended_tiles": []
        }