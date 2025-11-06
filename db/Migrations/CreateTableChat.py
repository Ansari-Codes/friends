from db.Migrations.MIGRATIONS import TABLE_CHATS as TABLE
def up():
    return f"""
CREATE TABLE IF NOT EXISTS {TABLE} (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    from_id INTEGER NOT NULL,
    to_id INTEGER NOT NULL,
    content TEXT NOT NULL,
    msg_type TEXT DEFAULT 'txt',
    reply_to_id INTEGER,
    sent_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    seen_at DATETIME,
    status TEXT CHECK(status IN ('seen','sent','pending','error')) DEFAULT 'pending',
    
    FOREIGN KEY (from_id) REFERENCES users(id),
    FOREIGN KEY (to_id) REFERENCES users(id),
    FOREIGN KEY (reply_to_id) REFERENCES {TABLE}(id)
);
"""

def down():
    return f"""
DROP TABLE IF EXISTS {TABLE};
"""
