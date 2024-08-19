from backend.database import db_keys
from backend.database.db_keys import k_user_table, k_song_table, k_bot_conf_table, k_type, k_value, k_karaoke_table, \
  k_work_id, k_status, k_mode, k_signal_table
from backend.database.entitys.y_signal import ySignal
from backend.database.entitys.y_user import yUser

# значение ячейки должно быть в " если там стринг, иначе no such column error


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



sql_create_signal_table = get_sql_create_table(k_signal_table,ySignal)
# sql_create_sont_table = get_sql_create_table(k_song_table, ySunoWork)

# sql_create_audio_table = '''
# CREATE TABLE `audio` (
#   `id` INTEGER PRIMARY KEY,
#   `idmus` int(11) NOT NULL,
#   `file` varchar(128) NOT NULL,
#   `cover` text NOT NULL,
#   `status` int(11) NOT NULL DEFAULT 0,
#   `userid` text NOT NULL
# );'''
# sql_create_karaoke_table = f""" CREATE TABLE IF NOT EXISTS {k_karaoke_table} (
#                                          `id` INTEGER PRIMARY KEY AUTOINCREMENT,
#                                          `{k_user_id}` text ,
#                                          `{k_work_id}` text ,
#                                          `{k_status}` int(11),
#                                          `{k_mode}` text
#                                      );"""
# sql_create_musicstyle_table = '''CREATE TABLE `musicstyle` (
#   `id` int(11) NOT NULL,
#   `style` varchar(64) NOT NULL
# );'''
# sql_create_payment_table = '''CREATE TABLE `payments` (
#   `id` INTEGER PRIMARY KEY,
#   `userid` int(11) NOT NULL,
#   `product` varchar(64) NOT NULL,
#   `price` int(11) NOT NULL,
#   `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
# );'''

sql_create_confn_table = f""" CREATE TABLE IF NOT EXISTS {k_bot_conf_table} (
`id` INTEGER PRIMARY KEY,
                                         {k_type} text,
                                         {k_value} text
                                     ); """




create_tables_list = [sql_create_confn_table,sql_create_signal_table
                      # sql_create_users_table, sql_create_musicstyle_table,
                      # sql_create_payment_table,sql_create_sont_table,sql_create_audio_table,
                      # sql_create_karaoke_table
                      ]