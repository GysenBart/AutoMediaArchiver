import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    #sync_folder = "PATHVARIABLE"
    #dest_folder = "PATHVARIABLE"

    sync_folder = os.path.join(basedir, "files/Camera")
    dest_folder = os.path.join(basedir, "files/Photos")
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')