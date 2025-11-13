from typing import Any, Dict
import httpx
import asyncio
import logging
from db.Migrations import CreateTableChat, CreateTableUsers

logger = logging.getLogger(__name__)

API_URL = "http://worldofansari.com/dbapi"

async def RUN_SQL(query: str, to_fetch: bool = False):
    payload = {"query": query, "to_fetch": to_fetch, "name": "friends"}
    try:
        print("started")
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.post(API_URL, json=payload)
            response.raise_for_status()
            print("finished")
            return response.json().get("data", [])
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error while calling API: {e.response.status_code} - {e.response.text}")
        raise
    except httpx.RequestError as e:
        logger.error(f"Request failed: {e}")
        raise
    except Exception as e:
        logger.exception("Unexpected error in RUN_SQL")
        raise
    finally:
        print("finished with error")

