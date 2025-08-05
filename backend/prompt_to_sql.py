import os
from backend.database_methods import tracks_schema, genres_schema, track_genres_schema, get_all_genres
import sqlglot
from sqlglot import parse_one, exp
from groq import Groq

def convert_user_prompt_to_sql_query(user_prompt, conn):

    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"""You're a SQLite query generator. The user will input a natural language prompt, and you will generate a valid SQL query. The instructions at the very end of the prompt are of utmost importance! Here's the database schema being used:
{tracks_schema, 
 genres_schema, 
 track_genres_schema}

Instructions:
- Only use the columns listed.
- Sort results by listen_count.
- Always select t.id, t.title, t.artist, t.album, t.listener_count
- Use JOINs instead of scraped_from_genre to if the prompt requires filtering by genre
- If the user mentions unsupported fields (chords, bpm, etc.), include a comment in the SQL explaining that a particular filter is ignored.
- Return only the SQL query (and comment if needed), no instructions.
- No semicolons!
- Return the top 5 results.
- No INSERT, UPDATE, DELETE, DROP, ALTER, TRUNCATE, CREATE, MERGE, REPLACE, ATTACH, DETACH, PRAGMA; you're only allowed to read the database (and therefore, allowed to filter, search, etc.)!

Prompt:
{user_prompt}

Also, here's a list of genres from the database:
{get_all_genres(conn)}

""",
        }
    ],
    model="llama-3.3-70b-versatile",
    )

    return chat_completion.choices[0].message.content

def validate_sql_query(sql_query: str) -> bool:
    FORBIDDEN_KEYWORDS = {
        "INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "TRUNCATE", "CREATE",
        "MERGE", "REPLACE", "ATTACH", "DETACH", "PRAGMA"}
    
    try:
        expression = parse_one(sql_query, read='sqlite')

        # check that the query contains a SELECT expression
        if not expression.find(exp.Select):
            return False

        # rejecting aggregate functions
        for func in expression.find_all(exp.Func):
            if func.name.upper() in {"SUM", "COUNT", "AVG", "MIN", "MAX"}:
                print("Query is aggragating")
                return False

        # checking for forbidden keywords
        upper_query = sql_query.upper()
        if any(keyword in upper_query for keyword in FORBIDDEN_KEYWORDS):
            print("Forbidden keyword found")
            return False

        # Prevent semicolon to avoid stacked statements
        if ";" in sql_query:
            print("Semi-colon found")
            return False

        return True

    except sqlglot.errors.ParseError:
        return False