# backend/main.py (Optimized for Free Tier)
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
import os
import time

app = FastAPI(title="AI Scene Finder API", version="1.0.0")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, replace with your blog URL
    allow_methods=["*"],
    allow_headers=["*"],
)

class SceneSearchRequest(BaseModel):
    url: str
    description: str
    filters: Optional[dict] = None

class SceneResult(BaseModel):
    timestamp: str
    start_time: str
    end_time: str
    confidence: float
    description: str
    thumbnail: Optional[str] = None

class SearchResponse(BaseModel):
    movie_title: str
    total_scenes: int
    processing_time: float
    scenes: List[SceneResult]

# Simple AI simulation (replace with real AI model)
def analyze_scene_simple(description: str, url: str):
    """Lightweight scene analysis for free tier"""
    keywords = {
        'action': ['fight', 'battle', 'chase', 'explosion', 'combat', 'punch'],
        'romance': ['kiss', 'love', 'romance', 'hug', 'proposal'],
        'drama': ['argument', 'confession', 'emotional', 'crying'],
        'comedy': ['joke', 'funny', 'laugh', 'comedy', 'prank']
    }
    
    desc_lower = description.lower()
    scene_type = 'general'
    confidence = 0.8
    
    for key, words in keywords.items():
        if any(word in desc_lower for word in words):
            scene_type = key
            confidence = min(0.9, confidence + 0.1)
            break
    
    # Generate realistic timestamps
    scenes = [
        {
            "timestamp": "00:15:30",
            "start_time": "00:15:30",
            "end_time": "00:18:45",
            "confidence": confidence,
            "description": f"{scene_type.title()} scene matching your description",
            "thumbnail": get_thumbnail_url(url)
        },
        {
            "timestamp": "01:22:15",
            "start_time": "01:22:15", 
            "end_time": "01:25:30",
            "confidence": confidence - 0.15,
            "description": f"Alternate {scene_type} sequence",
            "thumbnail": get_thumbnail_url(url)
        }
    ]
    
    return scenes

def get_thumbnail_url(url: str) -> str:
    """Extract thumbnail from YouTube URL"""
    if 'youtube.com' in url or 'youtu.be' in url:
        video_id = extract_youtube_id(url)
        if video_id:
            return f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
    return ""

def extract_youtube_id(url: str) -> str:
    """Extract YouTube video ID from URL"""
    import re
    patterns = [
        r'(?:youtube\.com\/watch\?v=|\/v\/|\.be\/)([^&?\n]+)',
        r'youtube\.com\/embed\/([^&?\n]+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return ""

@app.post("/api/v1/search", response_model=SearchResponse)
async def search_scenes(request: SceneSearchRequest):
    start_time = time.time()
    
    try:
        # Simulate processing (remove in production)
        import asyncio
        await asyncio.sleep(1)
        
        scenes = analyze_scene_simple(request.description, request.url)
        
        # Apply filters if provided
        if request.filters:
            min_confidence = request.filters.get('min_confidence', 0)
            scenes = [s for s in scenes if s['confidence'] >= min_confidence]
        
        processing_time = time.time() - start_time
        
        return SearchResponse(
            movie_title="YouTube Video",
            total_scenes=len(scenes),
            processing_time=round(processing_time, 2),
            scenes=scenes
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "AI Scene Finder API", "status": "running"}

@app.get("/api/v1/health")
async def health_check():
    return {"status": "healthy", "timestamp": time.time()}

# For serverless compatibility
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
