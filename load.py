#!/bin/python3
import sqlite3
import settings
import os
import sys

DB_SCHEMA = '''
CREATE TABLE IF NOT EXISTS "ACL" (
    "ENTRY"	TEXT NOT NULL UNIQUE,
    PRIMARY KEY("ENTRY")
);
CREATE UNIQUE INDEX IF NOT EXISTS "ENTRY_IDX" ON "ACL" (
    "ENTRY"	ASC
);
'''

if os.path.isfile(settings.LOCK_FILE):
    print('Cannot run, lockfile still exists: ' + str(settings.LOCK_FILE))
    sys.exit(1)
else:
    open(settings.LOCK_FILE, 'w+')
db = sqlite3.connect(settings.DB_FILE)
c = db.cursor()
c.executescript(DB_SCHEMA)
c.execute('DELETE FROM ACL')
db.commit()

with open(settings.ACL_FILENAME, 'r') as fd:
    entries = fd.read().split('\n')
    conv = []
    print('Processing ' + str(len(entries)) + ' entries...')
    for e in entries:
        if e != '':
            conv += [(e,)]
    c.executemany('REPLACE INTO ACL (ENTRY) VALUES (?)', conv)
db.commit()

os.remove(settings.LOCK_FILE)
