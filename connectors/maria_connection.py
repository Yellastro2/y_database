import mariadb
from mariadb import Connection

import private_conf


def get_con() -> Connection:
  try:
    conn = mariadb.connect(
      host=private_conf.some_args.get('mysql_host'),
      user=private_conf.some_args.get('mysql_user'),
      password=private_conf.some_args.get('mysql_pass'),
      database=private_conf.some_args.get('mysql_db')

    )
  except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")