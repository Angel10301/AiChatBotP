from fastapi import FastAPI
from pydantic import BaseModel
import logging
from utils import scrape_website, search_with_ollama
# FastAPI application module defining RESTful endpoints for web scraping and parsing.
# This file serves as the backend API, interfacing with the utils module.
# Date: June 10, 2025

app = FastAPI()
logging.basicConfig(level=logging.INFO, filename="api.log")

class ScrapeRequest(BaseModel):
    """Pydantic model for validating scrape request data.
    
    Attributes: 
        url (str): This URL to scrape.
        """
    url: str

@app.post("/scrape")
async def scrape_endpoint(request: ScrapeRequest):
    """Handle POST requests to scrape a website.
    
    Args:
        request (ScrapeRequest): Pydantic model containing the URL.
    
    Returns:
        dict: Response with scraped content or error message.
    
    Status Codes:
        200: Success with HTML content.
        500: Internal server error if scraping fails.
    """
    try:
        result = scrape_website(request.url)
        if result:
            logging.info("Scraping successful")
            return {"content": result, "status": "success"}
        logging.error("Scraping failed")
        return {"error": "Scraping failed", "status": "error"}, 500
    except Exception as e:
        logging.error(f"Exception: {e}")
        return {"error": str(e), "status": "error"}, 500

class ParseRequest(BaseModel):
    """Pydantic model for validating parse request data.
    
    Attributes:
        content (list[str]): List of text chunks to parse.
        query (str): Description of the information to extract.
    """
    content: list[str]
    query: str

@app.post("/parse")
async def parse_endpoint(request: ParseRequest):
    """Handle POST requests to parse content using LLM.
    
    Args:
        request (ParseRequest): Pydantic model containing content and query.
    
    Returns:
        dict: Response with parsed result or error message.
    
    Status Codes:
        200: Success with parsed result.
        500: Internal server error if parsing fails.
    """
    try:
        result = search_with_ollama(request.content, request.query)
        logging.info("Parsing successful")
        return {"result": result, "status": "success"}
    except Exception as e:
        logging.error(f"Exception: {e}")
        return {"error": str(e), "status": "error"}, 500