import time
import traceback

import mysql
from mysql.connector import MySQLConnection
from mysql.connector.cursor import MySQLCursor

import private_conf
from y_database.y_db_helper import yDbHelper

db_vers = 1

# conn: Connection

all_conns = {}

def get_con(f_type = 'sqlite'):
  '''

  :param f_type: 'sqlite' | 'mysql'
  :return:
  '''

  from y_database.connectors.mysql_connection import get_con

  all_conns[f_type] = get_con()
  return all_conns[f_type]

# conn = get_con()



class DbHelper(yDbHelper):
  conn: MySQLConnection
  cur: MySQLCursor
  is_connected = False

  key_val = '%s'

  def __init__(self, f_type='sqlite'):
    super().__init__()
    # self.conn = get_con(f_type)
    self.connection_pool = mysql.connector.pooling.MySQLConnectionPool(
      pool_name="inventory_pool",
      host=private_conf.some_args.get('mysql_host'),
      user=private_conf.some_args.get('mysql_user'),
      password=private_conf.some_args.get('mysql_pass'),
      database=private_conf.some_args.get('mysql_db')
    )
    # self.cur = self.conn.cursor()



  def close(self):
    try:
      # self.cur.close()
      self.cur.fetchall()
      pass
    except:
      pass

  def execute_sql(self,SQL,valls: tuple, cur = ""):
    print(f'EXECUTE SQL: {SQL}')
    is_exclusive_cursor = False
    if not cur:
      is_exclusive_cursor = True

      # cur = self.conn.cursor()
  # with self.conn.cursor(buffered=True) as cur:
  #   self.conn = get_con()

    connection = self.connection_pool.get_connection()
    cur = connection.cursor()

    # try:
    #   cur = self.conn.cursor()
    #   self.is_connected = True
    # except Exception as e:
    #   print(traceback.format_exc())

    try:
      cur.execute(SQL, valls)
    except Exception as e:
      print(traceback.format_exc())

    return cur, connection

  def fetch_result(self,cur: MySQLCursor,
                   conn ,
                   type = 'single'):

    # cur.stored_results()

    try:
      if type == 'single':
        f_result = cur.fetchone()
      else:
        f_result = cur.fetchall()
    except Exception as e:
      print(traceback.format_exc())


    cur.close()
    conn.close()
    return f_result

  def get_rows_by_coll(self, f_table, f_coll, f_vall, cur = ""):
    f_sql = f"SELECT * FROM {f_table} WHERE {f_coll} = {self.key_val}"
    # result = self.cur.execute(,
    #                              (f_vall,))
    # return result.fetchall()

    cur, conn = self.execute_sql(f_sql, (f_vall,), cur)
    return self.fetch_result(cur,conn, 'all')

  def get_rows_by_colls(self, f_table, f_colls: dict, cur = ""):
    f_sql = f"SELECT * FROM {f_table} WHERE "
    f_params = []
    for q_coll in f_colls.keys():
      f_sql += f"{q_coll} = ? AND "
      f_params.append(f_colls[q_coll])

    f_sql = f_sql.removesuffix(" AND ")
    result = self.cur.execute(f_sql,
                                 f_params)
    cur, conn = self.execute_sql(f_sql, f_params, cur)
    return self.fetch_result(cur,conn, 'all')

  def get_row_by_coll(self, table, coll, coll_vall,cur = ""):

    f_sql = f"SELECT * FROM `{table}` WHERE `{coll}` = %s"
    cur, conn = self.execute_sql(f_sql, (coll_vall,), cur)
    return self.fetch_result(cur,conn, 'single')

  def get_rows_by_coll_in(self,f_table,f_coll,f_vall,cur = ""):
    f_valstr = ''
    for q_val in f_vall:
      f_valstr += f'{self.key_val},'

    f_valstr = f_valstr.removesuffix(',')
    f_sql = f"SELECT * FROM {f_table} WHERE {f_coll} IN ({f_valstr})"
    cur, conn = self.execute_sql(f_sql,f_vall,cur)
    return self.fetch_result(cur,conn,'all')
    # result =  cur.fetchall()

    # result = self.cur.execute(f_sql,
    #                              f_vall)
    # return result.fetchall()


  def get_cell_by_coll(self, table, coll, coll_val, f_cell,cur = ""):
    SQL = f"SELECT `{f_cell}` FROM `{table}` WHERE `{coll}` = %s;"
    cur, conn = self.execute_sql(SQL, (coll_val,), cur)
    return self.fetch_result(cur,conn, 'single')
    # with self.conn.cursor(buffered=True) as cur:
    #   cur.execute(SQL,(coll_val,))
    #
    #   result = cur.fetchone()[0]
    #   # cur.close()
    #   return result

  def get_table(self, f_table):
    f_sql = f"SELECT * FROM `{f_table}`;"
    # with self.conn.cursor(buffered=True) as cur:
    # result = self.cur.execute(f_sql)
    # return self.cur.fetchall()
    cur, conn = self.execute_sql(f_sql, (), self.cur)
    return self.fetch_result(cur,conn, 'all')

  def get_table_cells(self,table,cell,cur = ""):
    SQL = f"SELECT `{cell}` FROM `{table}` "
    cur, conn = self.execute_sql(SQL, (), cur)
    result = []
    for q_fetch in self.fetch_result(cur,conn, 'all'):
      result.append(q_fetch[0])
    return result
    # with self.conn.cursor(buffered=True) as cur:
    #   cur.execute(SQL)
    #   result = []
    #   for q_fetch in cur.fetchall():
    #     result.append(q_fetch[0])
    #   return result

  def get_cells_by_colls(self, table, coll, coll_val: list, f_cell):

    f_valstr = ''
    # f_vall = str(f_vall)
    for q_val in coll_val:
      f_valstr += f'%s,'

    f_valstr = f_valstr.removesuffix(',')
    # f_sql = f"SELECT * FROM {f_table} WHERE {f_coll} IN ({f_valstr})"
    SQL = f"SELECT {f_cell} FROM `{table}` WHERE `{coll}` IN ({f_valstr})"
    result = self.cur.execute(SQL,
                              coll_val)
    return self.cur.fetchall()



  def row_exists(self,table,coll,coll_val):
      #Проверяем, есть ли юзер в базе
      self.cur.execute(f"SELECT `id` FROM `{table}` WHERE `{coll}` = ?", (coll_val,))
      try:
          f_res = self.get_row_by_coll(table,coll,coll_val)
          return bool(len(f_res))
      except:
          return False

  def get_coll(self, f_table, f_coll):
    f_sql = f"SELECT {f_coll} FROM {f_table}"
    result = self.cur.execute(f_sql)
    return result.fetchall()



  def delete_row_by_coll(self, f_table, coll, coll_vall):
    self.cur.execute(f"DELETE FROM `{f_table}` WHERE `{coll}` = ?", (coll_vall,))
    self.conn.commit()

  def delete_row(self, f_table, f_id):
    self.cur.execute(f"DELETE FROM `{f_table}` WHERE `id` = '{f_id}'")
    self.conn.commit()

  def get_all_cells_by_coll(self, table, coll, coll_val, f_cell):
    SQL = f"SELECT * FROM `{table}` WHERE `{coll}` = '{coll_val}'"
    result = self.cur.execute(SQL)
    return result.fetchall()


  def get_cell_num_by_coll(self,table,coll,coll_val,f_cell):
    try:
      f_res = self.get_cell_by_coll(table,coll,coll_val,f_cell)
      f_res = float(f_res)
    except:
      f_res = 0

    return f_res





  def get_row_by_coll_part(self,f_table,f_coll,f_vall):

    f_sql = f"SELECT * FROM {f_table} WHERE {f_coll} LIKE '%{f_vall}%'"
    result = self.cur.execute(f_sql,(f_vall,))
    return result.fetchone()



  def get_rows_by_coll(self, f_table, f_coll, f_vall):
    result = self.cur.execute(f"SELECT * FROM {f_table} WHERE {f_coll} = ?",
                                 (f_vall,))
    return result.fetchall()



  def add_row(self, table, data):
    f_sql = f'INSERT INTO `{table}` ('
    f_values = ''
    f_val_array = []
    for q_key in data.keys():
      f_sql += f'{self.key_val},'
      # f_values += f"'{data[q_key]}',"
      f_values += f"{self.key_val},"

      # f_val_array.append(q_key)
      f_val_array.append(str(data[q_key]))

    f_val_array = list(data.keys()) + f_val_array

    f_sql = f_sql.removesuffix(', ')
    f_values = f_values.removesuffix(',')
    f_sql += f") VALUES ({f_values})"
    f_some = self.cur.execute(f_sql, f_val_array)
    f_last_id = self.cur.lastrowid
    self.conn.commit()
    return f_last_id

  def upd_row_by_coll(self, table, coll, coll_vall, data):
    f_sql = f'UPDATE "{table}" SET '
    f_values = ()
    for q_key in data.keys():
      f_sql += f'"{q_key}" = ? , '
      f_values += data[q_key],

    f_sql = f_sql.removesuffix(', ')
    f_sql += f"WHERE `{coll}` = ?"
    f_values += coll_vall,
    self.cur.execute(f_sql, f_values)
    return self.conn.commit()

  def add_cell_by_coll(self, table, coll, coll_val, cell, cell_vall):

    try:
      f_vals = (cell_vall, coll_val)
      f_dbadm = self.get_cell_by_coll(table, coll, coll_val, cell)
      self.cur.execute(f"UPDATE `{table}` SET `{cell}` = ? WHERE `{coll}` = ?",f_vals)
    except Exception as e:
      f_vals = (coll_val, cell_vall)
      f_sql = f"INSERT INTO `{table}` (`{coll}`, `{cell}`) VALUES (?, ? )"
      self.cur.execute(f_sql,f_vals)
    return self.conn.commit()




# def update_con():
#   global conn
#   conn = get_con()



