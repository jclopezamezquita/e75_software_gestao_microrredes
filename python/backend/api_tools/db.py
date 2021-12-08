import os
from flask_sqlalchemy import SQLAlchemy
from pathlib import Path


DB_URI = 'mysql+pymysql://{}:{}@{}/{}'.format(
    os.getenv('DB_USER', 'flask'),
    os.getenv('DB_PASSWORD', ''),
    os.getenv('DB_HOST', 'mysql'),
    os.getenv('DB_NAME', 'flask')
)
db_config = {
    'SQLALCHEMY_DATABASE_URI': DB_URI,
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
}

db = SQLAlchemy()
