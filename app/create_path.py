def create_p(app, filename, folder=False):
    """
        return path to file if folder=False
        else retur path to folder with file
    """
    if not folder:
        return app.config['UPLOAD_FOLDER'] + '/' + filename[:2] + '/' + filename
    else:
        return app.config['UPLOAD_FOLDER'] + filename[:2] + '/'