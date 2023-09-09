#!/bin/python3
import os.path
import sqlite3
import settings
import time

db = sqlite3.connect(settings.DB_FILE)
c = db.cursor()

while True:
    try:
        raw_inp = input()

        inp = raw_inp.split(' ')[0] # skip everything after the first field

        if os.path.isfile(settings.LOCK_FILE):
            for _ in range(0, settings.LOCK_FILE_TIMEOUT_SECS):
                if os.path.isfile(settings.LOCK_FILE):
                    time.sleep(1)
                else:
                    break
            if os.path.isfile(settings.LOCK_FILE):
                raise ValueError('Lockfile still exists')

        if len(c.execute('select 1 from ACL where ACL.entry =?;', (inp,)).fetchall()) > 0:
            print('OK')
        else:
            print('ERR')
    except Exception:
        print('BH')
