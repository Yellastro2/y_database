import logging
import traceback
from sqlite3 import Connection, Cursor

from y_database.connectors import sqlite_connection
from y_database.db_confings import default_name
from y_database.y_db_helper import yDbHelper

db_vers = 1



# conn: Connection

all_conns = {}

def get_con(f_type = 'sqlite'):
  '''

  :param f_type: 'sqlite' | 'mysql'
  :return:
  '''

  from y_database.connectors.sqlite_connection import get_con

  all_conns[f_type] = sqlite_connection.get_con()
  return all_conns[f_type]

def get_db_connection(f_name = default_name):
  all_conns[f_name] = sqlite_connection.get_con(f_name)
  return all_conns[f_name]




class DbHelper(yDbHelper):
  # conn: Connection

  def __init__(self):
    super().__init__()
    # self.conn = get_db_connection()
    # self.cur = self.conn.cursor()


  def fetch_one(self, SQL, f_vals: tuple|list = ()):
    cur, conn = self.execute_sql(SQL, f_vals)
    f_res = cur.fetchone()[0]
    cur.close()
    conn.close()
    return f_res

  def fetch_row(self, SQL, f_vals: tuple|list = ()):
    cur, conn = self.execute_sql(SQL, f_vals)
    f_res = cur.fetchone()
    cur.close()
    conn.close()
    return f_res

  def fetch_all(self, SQL, f_vals: tuple|list = ()):

    cur, conn = self.execute_sql(SQL, f_vals)
    f_res = cur.fetchall()
    cur.close()
    conn.close()
    return f_res


  def commit(self, SQL, f_vals: tuple|list = ()):
    cur, conn = self.execute_sql(SQL, f_vals)
    f_last_id = cur.lastrowid
    conn.commit()
    cur.close()
    conn.close()
    return f_last_id



  def execute_sql(self, SQL, valls: tuple = (), cur=""):
    # print(f'EXECUTE SQL: {SQL}')

    connection = sqlite_connection.get_con(default_name)
    cur = connection.cursor()
    f_result = ''
    try:
      f_result = cur.execute(SQL, valls)
    except Exception as e:
      print(traceback.format_exc())

    # finally:
    #   cur.close()
      # connection.close()

    return f_result , connection


  def get_cur(self):
    connection = sqlite_connection.get_con(default_name)
    cur = connection.cursor()

    return cur, connection

  def close(self):
    try:
      pass
    except:
      pass

  def get_cells_by_colls(self,table, coll, coll_val:list, f_cell):

    f_valstr = ''
    for q_val in coll_val:
      f_valstr += f'?,'

    f_valstr = f_valstr.removesuffix(',')
    SQL = f"SELECT * FROM `{table}` WHERE `{coll}` IN ({f_valstr})"
    return self.fetch_all(SQL,coll_val)

  def get_cell_by_coll(self, table, coll, coll_val, f_cell):
    SQL = f"SELECT `{f_cell}` FROM `{table}` WHERE `{coll}` = '{coll_val}'"
    # # result = self.cur.execute(SQL)
    # cur, conn = self.execute_sql(SQL)
    # f_res = cur.fetchone()[0]
    # cur.close()
    # conn.close()
    return self.fetch_one(SQL)

  def row_exists(self,table,coll,coll_val):
      #Проверяем, есть ли юзер в базе
      # self.cur.execute(f"SELECT `id` FROM `{table}` WHERE `{coll}` = ?", (coll_val,))

      try:
          f_res = self.get_row_by_coll(table,coll,coll_val)
          return bool(len(f_res))
      except:
          return False

  def get_coll(self, f_table, f_coll):
    SQL = f"SELECT {f_coll} FROM {f_table}"
    # cur, conn = self.execute_sql(SQL)
    # f_res = cur.fetchall()
    # cur.close()
    # conn.close()
    return self.fetch_all(SQL)

  def get_table(self, f_table):
    SQL = f"SELECT * FROM `{f_table}`;"
    # cur, conn = self.execute_sql(SQL)
    # f_res = cur.fetchall()
    # cur.close()
    # conn.close()
    return self.fetch_all(SQL)

  def delete_row_by_coll(self, f_table, coll, coll_vall):
    SQL = f"DELETE FROM `{f_table}` WHERE `{coll}` = ?"
    # self.cur.execute(, )
    # self.conn.commit()
    # cur, conn = self.execute_sql(SQL,(coll_vall,))
    # f_comm = conn.commit()
    # cur.close()
    # conn.close()
    return self.commit(SQL, (coll_vall,))

  def delete_row(self, f_table, f_id):
    SQL = f"DELETE FROM `{f_table}` WHERE `id` = '{f_id}'"
    # self.cur.execute(, )
    # self.conn.commit()
    # cur, conn = self.execute_sql(SQL)
    # f_comm = conn.commit()
    # cur.close()
    # conn.close()
    return self.commit(SQL)
    # self.cur.execute()
    # self.conn.commit()

  def get_all_cells_by_coll(self, table, coll, coll_val, f_cell):
    SQL = f"SELECT * FROM `{table}` WHERE `{coll}` = '{coll_val}'"
    # result = self.cur.execute(SQL)
    # return result.fetchall()
    # cur, conn = self.execute_sql(SQL)
    # f_res = cur.fetchall()
    # cur.close()
    # conn.close()
    return self.fetch_all(SQL)


  def get_cell_num_by_coll(self,table,coll,coll_val,f_cell):
    try:
      f_res = self.get_cell_by_coll(table,coll,coll_val,f_cell)
      f_res = float(f_res)
    except:
      f_res = 0

    return f_res

  def get_row_by_coll(self, table, coll, coll_vall):
    SQL = f"SELECT * FROM {table} WHERE {coll} = ?"
    # cur, conn = self.execute_sql(SQL, (coll_vall,))
    # f_res = cur.fetchone()
    # cur.close()
    # conn.close()
    return self.fetch_row(SQL, (coll_vall,))

    # result = self.cur.execute()
    # return result.fetchone()



  def get_row_by_coll_part(self,f_table,f_coll,f_vall):


    SQL = f"SELECT * FROM {f_table} WHERE {f_coll} LIKE '%{f_vall}%'"
    # cur, conn = self.execute_sql(SQL,(f_vall,))
    # f_res = cur.fetchone()
    # cur.close()
    # conn.close()
    return self.fetch_row(SQL,(f_vall,))


  def get_rows_by_coll_in(self,f_table,f_coll,f_vall):
    f_valstr = ''
    # f_vall = str(f_vall)
    for q_val in f_vall:
      f_valstr += f'?,'

    f_valstr = f_valstr.removesuffix(',')
    SQL = f"SELECT * FROM {f_table} WHERE {f_coll} IN ({f_valstr})"

    # cur, conn = self.execute_sql(SQL, f_vall)
    # f_res = cur.fetchall()
    # cur.close()
    # conn.close()
    return self.fetch_all(SQL, f_vall)
    #
    # result = self.cur.execute(f_sql,
    #                              f_vall)
    # return result.fetchall()

  def get_rows_by_coll(self, f_table, f_coll, f_vall):

    SQL = f"SELECT * FROM {f_table} WHERE {f_coll} = ?"
    # f_res, conn = self.execute_sql(SQL, (f_vall,))
    # conn.close()
    return self.fetch_all(SQL, (f_vall,))
    #
    # result = self.cur.execute(,
    #                              )
    # return result.fetchall()

  def get_rows_by_colls(self, f_table, f_colls: dict):
    SQL = f"SELECT * FROM {f_table} WHERE "
    f_params = []
    for q_coll in f_colls.keys():
      SQL += f"{q_coll} = ? AND "
      f_params.append(f_colls[q_coll])

    SQL = SQL.removesuffix(" AND ")

    # f_res, conn = self.execute_sql(SQL, f_params)
    # conn.close()
    return self.fetch_all(SQL, f_params)

    # result = self.cur.execute(f_sql,
    #                              f_params)
    # return result.fetchall()

  def add_row(self, table, data):
    f_sql = f'INSERT INTO "{table}" ('
    f_values = ''
    f_val_array = []
    for q_key in data.keys():
      f_sql += f'"{q_key}", '
      # f_values += f"'{data[q_key]}',"
      f_values += f"?,"
      f_val_array.append(data[q_key])
    f_sql = f_sql.removesuffix(', ')
    f_values = f_values.removesuffix(',')
    f_sql += f") VALUES ({f_values})"
    # f_some = self.cur.execute(f_sql, f_val_array)


    # f_res, conn = self.execute_sql(f_sql, f_val_array)
    # f_last_id = f_res.lastrowid
    # conn.commit()
    # conn.close()
    # return f_last_id
    return self.commit(f_sql, f_val_array)
    #
    # self.conn.commit()
    # return f_last_id


  def upd_row_by_coll(self, table, coll, coll_vall, data):
    f_sql = f'UPDATE "{table}" SET '
    f_values = ()
    for q_key in data.keys():
      f_sql += f'"{q_key}" = ? , '
      f_values += data[q_key],

    f_sql = f_sql.removesuffix(', ')
    f_sql += f"WHERE `{coll}` = ?"
    f_values += coll_vall,

    # f_res, conn = self.execute_sql(f_sql, f_values)
    # conn.commit()
    # conn.close()
    return self.commit(f_sql, f_values)


    # self.cur.execute(f_sql, f_values)
    # return self.conn.commit()

  def add_cell_by_coll(self, table, coll, coll_val, cell, cell_vall):

    try:
      f_vals = (cell_vall, coll_val)
      f_dbadm = self.get_cell_by_coll(table, coll, coll_val, cell)
      SQL = f"UPDATE `{table}` SET `{cell}` = ? WHERE `{coll}` = ?"
      # f_res, conn = self.execute_sql(SQL,f_vals)
      self.commit(SQL,f_vals)
      # self.cur.execute(,f_vals)
    except Exception as e:
      f_vals = (coll_val, cell_vall)
      SQL = f"INSERT INTO `{table}` (`{coll}`, `{cell}`) VALUES (?, ? )"
      # f_res, conn = self.execute_sql(SQL, f_vals)
      f_new_id = self.commit(SQL, f_vals)
      return f_new_id
      # self.cur.execute(f_sql,f_vals)

    return -404
    # f_res, conn = self.execute_sql(SQL, coll_val)
    # f_commit = conn.commit()
    # conn.close()
    # return f_commit





