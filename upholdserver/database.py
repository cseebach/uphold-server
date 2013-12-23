__author__ = 'Cameron Seebach'

import json


def setup(db):
    db.executescript(
        """
        CREATE TABLE IF NOT EXISTS log (
            computer text,
            time text,
            data text
        );
        CREATE INDEX IF NOT EXISTS log_computer ON log ( computer );
        CREATE INDEX IF NOT EXISTS log_time ON log ( time );
        """
    )


def add_log_entry(db, entry):
    if "computer" in entry and "ran_at" in entry:
        row = entry["computer"], entry["ran_at"], json.dumps(entry)
        db.execute("INSERT INTO log VALUES(?,?,?);", row)
    elif "computer" in entry and "task" in entry:
        row = entry["computer"], entry["task"]["finished"], json.dumps(entry)
        db.execute("INSERT INTO log VALUES(?,?,?);", row)