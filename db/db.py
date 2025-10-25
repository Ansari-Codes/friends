from ENV import DB_CREDS
import aiosqlite
import logging

logger = logging.getLogger(__name__)

async def INIT_DB():
    """Initialize async database connection using ENV.DB_CREDS"""
    engine = DB_CREDS.get("ENGINE", "sqlite")
    if engine == "sqlite":
        conn = await aiosqlite.connect(DB_CREDS["NAME"])
        conn.row_factory = aiosqlite.Row  
        return conn
    raise NotImplementedError(f"Engine '{engine}' not supported yet.")

async def RUN_SQL(query: str, to_fetch: bool = False):
    """
    Run a SQL query asynchronously.
    
    Args:
        query (str): SQL query to execute
        to_fetch (bool): If True, fetch results for SELECT queries
        
    Returns:
        list[tuple] for SELECT queries if to_fetch=True, otherwise []
    """
    conn = await INIT_DB()
    try:
        async with conn.cursor() as cur:
            await cur.execute(query)
            if to_fetch:
                rows = await cur.fetchall()
                result = [dict(row) for row in rows]
            else:
                result = []
        await conn.commit()
        return result
    except Exception as e:
        await conn.rollback()
        logger.exception("SQL execution failed")
        raise e
    finally:
        await conn.close()
