import datetime
import traceback
from typing import Type

from y_database.db_helper import DbHelper
from y_database.db_keys import k_bot_conf_table, k_value, k_type
from y_database.entitys import yEntity


def get_sql_create_table(f_name,f_entity):


  f_result = f""" CREATE TABLE IF NOT EXISTS {f_name} (
                                           id integer PRIMARY KEY,\n"""

  f_param = f_entity.__dict__
  f_fields = f_param['__annotations__']
  for q_name in f_fields.keys():
    if q_name == 'id':
      continue
    q_field = f_fields[q_name]
    q_type = 'text'
    # print(q_field)
    if q_field is int:
      # print('its int')
      q_type = 'integer'

    f_result += f'`{q_name}` {q_type},'

  f_result = f_result.removesuffix(',')
  f_result += ');'

  return f_result


def update_db(f_db_entitys : list[Type[yEntity]],f_db = DbHelper()):
  print(f'Start init yDatabase')
  f_start = datetime.datetime.now().timestamp()

  f_db_gen_tables = {
  }

  for q_entity in f_db_entitys:
    f_db_gen_tables[q_entity.__name__] = q_entity


  # try:
  #   f_vers = int(f_db.get_cell_by_coll(k_bot_conf_table, k_type, 'db_version', k_value))
  # except:
  #   f_vers = -1
  # if f_vers < 1:
  #   try:
  #     for q_table in db_shema.create_tables_list:
  #       f_db.cur.execute(q_table)
  #     print('db created')
  #   except:
  #     print(traceback.format_exc())
  #
  #   f_db.add_cell_by_coll(k_bot_conf_table, k_type, 'db_version', k_value, db_vers)
  #
  #   print('success update db')

  print('check autogener tables, for now only coll count')

  for q_table in f_db_gen_tables.keys():
    q_obj_colls = f_db_gen_tables[q_table].__dict__['__annotations__']
    try:
      f_db.fetch_all(f'select * from {q_table}')
      # f_db.cur.execute(f'select * from {q_table}')
    except:
      q_creater = get_sql_create_table(q_table, f_db_gen_tables[q_table])

      f_db.commit(q_creater)
      # f_db.fetch_one(f'select * from {q_table}')

      # f_db.cur.execute(q_creater)
      # f_db.cur.execute(f'select * from {q_table}')

    cur, conn = f_db.get_cur()
    cur.execute(f'select * from {q_table}')
    q_table_colls = list(map(lambda x: x[0], cur.description))
    if_update=  False
    if len(q_obj_colls)+1 != len(q_table_colls):
      print(f'find different coll size in {q_table}')
      for q_key in q_obj_colls.keys():
        if q_key not in q_table_colls:
          print(f'find apsent coll {q_key} in {q_table}, type {q_obj_colls[q_key]}')
          q_type = 'text'
          # print(q_field)
          if q_obj_colls[q_key] is int:
            # print('its int')
            q_type = 'integer'
          cur.execute(f"alter table {q_table} add column '%s'  {q_type}"% q_key)
          conn.commit()
    cur.close()
    conn.close()
  f_db.close()

  f_end = round(datetime.datetime.now().timestamp() - f_start,4)

  print(f'yDatabase inited: {f_end} sec')



