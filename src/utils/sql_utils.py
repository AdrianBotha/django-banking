def run_sql_file(cur, file: str):
    with open(file, 'r') as f:
        sql = f.read()
        return cur.execute(sql)
