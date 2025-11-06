from db.db import RUN_SQL
from db.Migrations.CreateTableChat import up as ctcup
from db.Migrations.CreateTableUsers import up as ctuup
from asyncio import run

SQL = '\n'.join([ctcup(), ctuup()])
run(RUN_SQL(SQL))
