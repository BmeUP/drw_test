import shutil


def delete_folder(path):
    shutil.rmtree(path)

def check_owner(db, hashed_fn, user_info):
    cur = db().cursor()
    query = """
        select user_name, hashed_file_name from main  where 
        hashed_file_name=? and user_name=?
    """
    cur.execute(
            query, 
            [
                 hashed_fn, user_info.get('username')
            ]
        )
    res = cur.fetchall()
    return len(res) > 0

def delete_record(db, hashed_fn, user_info):
    cur = db().cursor()
    query = """
        delete from main  where 
        hashed_file_name=? and user_name=?
    """
    cur.execute(
            query, 
            [
                hashed_fn,
                user_info.get('username')
            ]
        )
    db().commit()