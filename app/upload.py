import hashlib
import mimetypes
import bcrypt


def allowed_file(filename):
    allowed_ext = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'docx'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_ext


def create_file_hash(file):
    file_hash_md5 = hashlib.md5()
    file_hash_md5.update(file.read())
    return file_hash_md5.hexdigest()


def generate_file_name(file):
    """
        return file name from hashed file name and mimetype
    """
    return '{}{}'.format(
            create_file_hash(file), 
            mimetypes.guess_extension(file.mimetype)
        )


def write_to_db(db, file_name, hashed_fn, user_info):
    query = """
        insert into main(file_name, hashed_file_name, user_name)
        values (?, ?, ?)
    """
    db().cursor().execute(
            query, 
            [
                file_name, hashed_fn,
                user_info.get('username')
            ]
        )
    db().commit()

