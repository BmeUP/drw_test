def get_file_name(db, hashed_file_name):
    cur = db().cursor()
    query = """
        select file_name from main  where 
        hashed_file_name =?
    """
    cur.execute(query, [hashed_file_name])
    res = cur.fetchall()
    db().close()
    return res