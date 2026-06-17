import mariadb
from mariadb import Connection

import env_configs


def get_con() -> Connection:
  try:
    conn = mariadb.connect(
      host=env_configs.some_args.get('mysql_host'),
      user=env_configs.some_args.get('mysql_user'),
      password=env_configs.some_args.get('mysql_pass'),
      database=env_configs.some_args.get('mysql_db')

    )
  except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")