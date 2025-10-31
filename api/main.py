from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.models import init_db, get_all_properties
from scraper.harrison_scraper import scrape_harrisons
from scraper.jordan_halstead_scraper import scrape_jordan_halstead

app = FastAPI(title="Property Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()

@app.get("/properties")
def list_properties():
    return get_all_properties()

@app.get("/scrape/harrisons")
def scrape_harrisons_route():
    return scrape_harrisons()

@app.get("/scrape/jordan-halstead")
def scrape_jordan_route():
    return scrape_jordan_halstead()
