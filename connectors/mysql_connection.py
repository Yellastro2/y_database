from mysql.connector import connect, Error

import env_configs


def get_con():
    conn =None
    try:
        conn = connect(
            host=env_configs.some_args.get('mysql_host'),
            user=env_configs.some_args.get('mysql_user'),
            password=env_configs.some_args.get('mysql_pass'),
            database=env_configs.some_args.get('mysql_db'))
        # IF ONLY Lost connection to MySQL server during query
        # with conn.cursor(buffered=True) as cur:
        #
        #     cur.execute('set global max_allowed_packet=67108864')
    except Error as e:
        print(e)

    return conn