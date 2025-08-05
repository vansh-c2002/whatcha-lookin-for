
DB_PATH = os.path.join(os.path.dirname(__file__), "song_database_trial.db")

class QueryRequest(BaseModel):
    prompt: str

@app.post("/query")
async def query_songs(request: QueryRequest):
    # 1. Convert prompt to SQL
    conn = sqlite3.connect(DB_PATH)
    sql_query = convert_user_prompt_to_sql_query(request.prompt, conn)
    if validate_sql_query(sql_query):
    # 2. Run SQL on the database
        try:
            cursor = conn.cursor()
            cursor.execute(sql_query)
            results = cursor.fetchall()
            # Only return top 5
            results = results[:5]