from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import importlib
from pydantic import BaseModel
import sqlite3
import os
from . import prompt_to_sql

importlib.reload(prompt_to_sql)

from .prompt_to_sql import convert_user_prompt_to_sql_query, validate_sql_query

from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Enable CORS for all origins (for local dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, set this to your frontend's URL, MAJOR TODO
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = os.path.join(os.path.dirname(__file__), "song_database.db")

class QueryRequest(BaseModel):
    prompt: str

@app.post("/query")
async def query_songs(request: QueryRequest):
    # 1. Convert prompt to SQL
    sql_query = convert_user_prompt_to_sql_query(request.prompt)
    if validate_sql_query(sql_query):
    # 2. Run SQL on the database
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute(sql_query)
            results = cursor.fetchall()
            # Only return top 5
            results = results[:5]
            # Only return title, artist, duration
            response = [
                {
                    "title": row[1],
                    "artist": row[2],
                    "duration": row[3]
                }
                for row in results
            ]
            conn.close()
            return {"results": response}
        except Exception as e:
            return {"error": str(e)}
    else:
        return {"error": "Unsafe SQL query"}