from fastapi import APIRouter
import sqlite3

router = APIRouter()

@router.get("/properties")
def get_properties():
    conn = sqlite3.connect("properties.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, title, price, bedrooms, bathrooms, location, image_url, description, url
        FROM properties
    """)

    rows = cursor.fetchall()
    conn.close()

    properties = []
    for row in rows:
        properties.append({
            "id": row[0],
            "title": row[1],
            "price": row[2],
            "bedrooms": row[3],
            "bathrooms": row[4],
            "location": row[5],
            "image_url": row[6],
            "description": row[7],
            "url": row[8],
        })
    
    return properties
