import sqlite3

def setup_database():
    with sqlite3.connect("database.sqlite3") as db:
        version = db.execute("PRAGMA user_version;").fetchone()[0]

        if version < 1:
            db.execute("""
                CREATE TABLE IF NOT EXISTS requests (
                    id      INTEGER PRIMARY KEY NOT NULL,
                    user_id INTEGER             NOT NULL,
                    phase   INTEGER             NOT NULL,

                    UNIQUE(user_id, phase)
                );
            """)

            db.execute("""
                CREATE TABLE IF NOT EXISTS request_content (
                    id         INTEGER PRIMARY KEY NOT NULL,
                    request_id INTEGER             NOT NULL,
                    content    TEXT                NOT NULL,
                    score      INTEGER             NOT NULL,

                    FOREIGN KEY (request_id) REFERENCES requests(request_id)
                );
            """)

            db.execute("""
                CREATE TABLE IF NOT EXISTS current_phase (
                    phase INTEGER PRIMARY KEY NOT NULL
                );
            """)
            db.execute("INSERT INTO current_phase (phase) VALUES (1)")

            db.execute("PRAGMA user_version = 1;")
        
        if version < 2:
            db.execute("""
                ALTER TABLE current_phase
                    ADD COLUMN active INTEGER NOT NULL DEFAULT 0;
            """)
            
            db.execute("PRAGMA user_version = 2;")
        
