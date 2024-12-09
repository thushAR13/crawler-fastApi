import aiohttp
from typing import Dict
import json
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
import uvicorn
import yaml

# Load configuration
with open("client_config.yaml", "r") as config_file:
    config = yaml.safe_load(config_file)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

def print_sitemap(sitemap: Dict[str, list], root_url: str, level: int = 0, visited=None) -> str:
    if visited is None:
        visited = set()
        
    output = []
    if level == 0:
        output.append(f"└── {root_url}")
        
    if root_url in sitemap and root_url not in visited:
        visited.add(root_url)
        for i, url in enumerate(sitemap[root_url]):
            is_last = i == len(sitemap[root_url]) - 1
            prefix = "    " * level
            connector = "└── " if is_last else "├── "
            output.append(f"{prefix}{connector}{url}")
            
            # Recurse into children, ensuring no duplicates
            if url in sitemap and url not in visited:
                child_output = print_sitemap(sitemap, url, level + 1, visited)
                output.append(child_output)
                
    return "\n".join(output)


async def crawl_site(url: str) -> Dict:
    async with aiohttp.ClientSession() as session:
        async with session.post(
            config["server_url"],
            json={"url": url}
        ) as response:
            return await response.json()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.post("/crawl", response_class=HTMLResponse)
async def crawl(request: Request, url: str = Form(...)):
    try:
        result = await crawl_site(url)
        tree_view = print_sitemap(result["sitemap"], url)
        json_view = json.dumps(result, indent=2)
        
        return templates.TemplateResponse("result.html", {
            "request": request,
            "tree_view": tree_view,
            "json_view": json_view
        })
    except Exception as e:
        return templates.TemplateResponse("result.html", {
            "request": request,
            "tree_view": f"Error: {str(e)}",
            "json_view": ""
        })

if __name__ == "__main__":
    uvicorn.run(app, host=config["host"], port=config["port"])