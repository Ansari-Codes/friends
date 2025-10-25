from ENV import DB_CREDS, MIGRATIONS_FOLDER
import asyncio
import aiosqlite
import importlib
import os
import sys
from pathlib import Path
from .db import RUN_SQL

# --- Migration management ---

BASE_DIR = Path(__file__).resolve().parent
MIGRATIONS_PATH = BASE_DIR / "migrations"
APPLIED_FILE = MIGRATIONS_PATH / ".applied"

def get_applied() -> set[str]:
    """Read already applied migrations."""
    if not APPLIED_FILE.exists():
        return set()
    return set(APPLIED_FILE.read_text().splitlines())

def mark_applied(name: str):
    """Mark a migration as applied."""
    with open(APPLIED_FILE, "a") as f:
        f.write(name + "\n")

def unmark_last():
    """Remove last migration from applied list."""
    applied = list(get_applied())
    if not applied:
        return None
    last = applied[-1]
    with open(APPLIED_FILE, "w") as f:
        f.write("\n".join(applied[:-1]))
    return last

# --- Core actions ---

async def apply_migrations():
    """Apply all pending migrations."""
    applied = get_applied()
    files = sorted(
        f[:-3]
        for f in os.listdir(MIGRATIONS_PATH)
        if f.endswith(".py") and not f.startswith("__")
    )
    if not files:
        print("⚠️  No migration files found.")
        return
    for file in files:
        if file in applied:
            continue
        print(f"🚀 Applying migration: {file}")
        try:
            mod = importlib.import_module(f"{MIGRATIONS_FOLDER}.{file}")
            sql = mod.up()
            await RUN_SQL(sql)
            mark_applied(file)
            print(f"✅ Applied: {file}")
        except Exception as e:
            print(f"❌ Failed migration {file}: {e}")
            break
    print("✨ Migrations complete.")

async def rollback_last():
    """Rollback the last applied migration."""
    last = unmark_last()
    if not last:
        print("❌ No migrations to rollback.")
        return
    print(f"🔄 Rolling back migration: {last}")
    try:
        mod = importlib.import_module(f"backend.{MIGRATIONS_FOLDER}.{last}")
        sql = mod.down()
        await RUN_SQL(sql)
        print("✅ Rollback complete.")
    except Exception as e:
        print(f"❌ Rollback failed: {e}")

# --- Command line interface ---

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m db.migrate [up|down]")
        sys.exit(1)
    cmd = sys.argv[1].lower()
    if cmd == "up":
        asyncio.run(apply_migrations())
    elif cmd == "down":
        asyncio.run(rollback_last())
    else:
        print("Unknown command. Use 'up' or 'down'.")
