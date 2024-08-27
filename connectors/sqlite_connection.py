import sqlite3
import traceback
from sqlite3 import Connection

def get_con() -> Connection:
  try:
    conn = sqlite3.connect('suno.db', check_same_thread=False)

  except:
    conn = None
    traceback.print_exc()
  return conn