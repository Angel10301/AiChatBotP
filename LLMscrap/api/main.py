from fastapi import FastAPI
from pydantic import BaseModel
from utils import scrape_website

app = FastAPI()

class ScrapeRequest(BaseModel):
    url: str

@app.post("/scrape")
async def scrape_endpoint(request: ScrapeRequest):
    result = scrape_website(request.url)
    if result:
        return {"content": result, "status": "success"}
    return {"error": "Scraping failed", "status": "error"}, 500