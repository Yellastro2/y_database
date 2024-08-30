from mysql.connector import connect, Error

import private_conf


def get_con():
    conn =None
    try:
        conn = connect(
            host=private_conf.some_args.get('mysql_host'),
            user=private_conf.some_args.get('mysql_user'),
            password=private_conf.some_args.get('mysql_pass'),
            database=private_conf.some_args.get('mysql_db'))
        # IF ONLY Lost connection to MySQL server during query
        # with conn.cursor(buffered=True) as cur:
        #
        #     cur.execute('set global max_allowed_packet=67108864')
    except Error as e:
        print(e)

    return conn