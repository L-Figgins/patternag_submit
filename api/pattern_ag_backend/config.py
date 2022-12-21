from os import getenv

class Config:
    """
    Flask configuration object
    """
    SECRET_KEY = getenv('SECRET_KEY', "")
    FLASK_APP = getenv("pattern_ag_backend")