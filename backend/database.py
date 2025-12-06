
import os
from dotenv import load_dotenv
import asyncpg

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

async def get_db_connection():
    """Establishes and returns an asyncpg database connection."""
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL environment variable is not set.")

    conn = None
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        if conn:
            await conn.close()
        raise

async def close_db_connection(conn):
    """Closes an asyncpg database connection."""
    if conn:
        await conn.close()

async def execute_query(query: str, *args):
    """Executes a given SQL query and returns the result."""
    conn = None
    try:
        conn = await get_db_connection()
        result = await conn.fetch(query, *args)
        return result
    finally:
        await close_db_connection(conn)

async def execute_insert(query: str, *args):
    """Executes an INSERT query and returns the ID of the new record."""
    conn = None
    try:
        conn = await get_db_connection()
        # Assuming the query uses 'RETURNING id' or similar
        record_id = await conn.fetchval(query, *args)
        return record_id
    finally:
        await close_db_connection(conn)

# Example usage (for testing, can be removed later)
async def test_db_connection():
    try:
        conn = await get_db_connection()
        if conn:
            print("✅ Successfully connected to the database.")
            await conn.close()
    except Exception as e:
        print(f"❌ Failed to connect to the database: {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_db_connection())
