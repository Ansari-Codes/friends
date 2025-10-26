class Query:
    def __init__(self, table: str):
        self.table = table
        self._action = None
        self._columns = []
        self._values = {}
        self._where = []
        self._limit = None
        self._order_by = None

    # --- INSERT ---
    def insert(self, **data):
        self._action = "insert"
        self._values = data
        return self

    # --- SELECT ---
    def select(self, *columns):
        self._action = "select"
        self._columns = columns or ["*"]
        return self

    # --- UPDATE ---
    def update(self, **data):
        self._action = "update"
        self._values = data
        return self

    # --- DELETE ---
    def delete(self):
        self._action = "delete"
        return self

    # --- ORDER BY ---
    def order_by(self, column, direction="ASC"):
        self._order_by = f"{column} {direction.upper()}"
        return self

    # --- LIMIT ---
    def limit(self, n: int):
        self._limit = n
        return self

    # --- WHERE ---
    def where(self, **conditions):
        """Base WHERE clause (replaces any previous conditions)."""
        conds = [self._build_condition(k, v) for k, v in conditions.items()]
        self._where = [f"({' AND '.join(conds)})"]
        return self

    def andWhere(self, **conditions):
        conds = [self._build_condition(k, v) for k, v in conditions.items()]
        self._where.append(f"AND ({' AND '.join(conds)})")
        return self

    def orWhere(self, **conditions):
        conds = [self._build_condition(k, v) for k, v in conditions.items()]
        self._where.append(f"OR ({' AND '.join(conds)})")
        return self

    # --- internal helper for condition building ---
    def _build_condition(self, key, value):
        if isinstance(value, str):
            return f"{key}='{value}'"
        elif isinstance(value, (tuple, list)) and len(value) == 2:
            # e.g. ("<", 10) or (">=", 5)
            return f"{key}{value[0]}{value[1]}"
        else:
            return f"{key}={value}"

    # --- SQL BUILDER ---
    def SQL(self) -> str:
        if self._action == "insert":
            cols = ", ".join(self._values.keys())
            def v_or_NULL(v): 
                return f"'{v}'" if v else 'NULL'
            vals = ", ".join(
                [f"{v_or_NULL(v)}" if isinstance(v, str) else str(v) for v in self._values.values()]
            )
            return f"INSERT INTO {self.table} ({cols}) VALUES ({vals});"

        if self._action == "select":
            cols = ", ".join(self._columns) if self._columns else "*"
            sql = f"SELECT {cols} FROM {self.table}"
            if self._where:
                sql += " WHERE " + " ".join(self._where)
            if self._order_by:
                sql += f" ORDER BY {self._order_by}"
            if self._limit:
                sql += f" LIMIT {self._limit}"
            return sql + ";"

        if self._action == "update":
            sets = ", ".join(
                [f"{k}='{v}'" if isinstance(v, str) else f"{k}={v}" for k, v in self._values.items()]
            )
            sql = f"UPDATE {self.table} SET {sets}"
            if self._where:
                sql += " WHERE " + " ".join(self._where)
            return sql + ";"

        if self._action == "delete":
            sql = f"DELETE FROM {self.table}"
            if self._where:
                sql += " WHERE " + " ".join(self._where)
            return sql + ";"

        raise ValueError("No action defined (insert/select/update/delete)")
