import os
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

# Points to the .env in your root folder
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

from fastapi import FastAPI
from run.routes.search import router as search_router
app = FastAPI(
    title="RAK Tiles AI API",
    version="1.0.0"
)

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# It is good practice to add a prefix so your URL is /api/search
app.include_router(search_router, prefix="/api")

# Mount static files for product images
image_dir = os.path.join(os.path.dirname(__file__), "data", "page_images")
app.mount("/images", StaticFiles(directory=image_dir), name="images")

@app.get("/")
async def root():
    return {"message": "RAK Tiles API is online"}