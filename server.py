from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
from crawler_service import WebCrawlerService
import uvicorn
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

app = FastAPI()
crawler = WebCrawlerService()

class CrawlRequest(BaseModel):
    url: HttpUrl

@app.get("/healthz")
async def healthz():
    return {"status": "ok"}

@app.post("/crawl")
async def crawl_url(request: CrawlRequest):
    logging.debug(f"Received crawl request for URL: {request.url}")
    try:
        sitemap = await crawler.crawl(str(request.url))
        logging.debug(f"Successfully generated sitemap for URL: {request.url}")
        return {"sitemap": sitemap}
    except Exception as e:
        logging.error(f"Error during crawling: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    logging.info("Starting FastAPI server on http://0.0.0.0:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)