import sqlite3
import traceback
from sqlite3 import Connection

def get_con(f_name = "some.db") -> Connection:
  try:
    conn = sqlite3.connect(f_name,
                           # check_same_thread=False,
                           timeout=1)

    conn.row_factory = sqlite3.Row

  except:
    conn = None
    traceback.print_exc()
  return conn