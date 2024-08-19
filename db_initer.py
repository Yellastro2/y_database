import traceback

from backend.database import db_shema
from backend.database.db_helper import DbHelper, db_vers
from backend.database.db_keys import k_bot_conf_table, k_type, k_value
from backend.database.entitys.y_signal import ySignal
from backend.database.entitys.y_user import yUser

s_db_entitys = [ySignal,yUser]
#
s_db_gen_tables = {
#   k_user_table: yUser,
#   k_song_table: ySunoWork
}

for q_entity in s_db_entitys:
  s_db_gen_tables[q_entity.__name__] = q_entity

# for q_entitys in s_db_entitys:
#   if not q_entitys in s_db_gen_tables.values():
#     s_db_gen_tables[q_entitys.__name__] = q_entitys

def update_db():

  f_db = DbHelper()
  try:
    f_vers = int(f_db.get_cell_by_coll(k_bot_conf_table, k_type, 'db_version', k_value))
  except:
    f_vers = -1
  if f_vers < 1:
    try:
      for q_table in db_shema.create_tables_list:
        f_db.cur.execute(q_table)
      print('db created')
    except:
      print(traceback.format_exc())

    f_db.add_cell_by_coll(k_bot_conf_table, k_type, 'db_version', k_value, db_vers)

    print('success update db')

  print('check autogener tables, for now only coll count')

  for q_table in s_db_gen_tables.keys():
    q_obj_colls = s_db_gen_tables[q_table].__dict__['__annotations__']
    try:
      f_db.cur.execute(f'select * from {q_table}')
    except:
      q_creater = db_shema.get_sql_create_table(q_table,s_db_gen_tables[q_table])
      f_db.cur.execute(q_creater)
      f_db.cur.execute(f'select * from {q_table}')
    q_table_colls = list(map(lambda x: x[0], f_db.cur.description))
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
          f_db.cur.execute(f"alter table {q_table} add column '%s'  {q_type}"% q_key)
          f_db.conn.commit()
  f_db.close()



