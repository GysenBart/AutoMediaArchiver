from app import db
from datetime import datetime, timezone


class ArchivedFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    filename = db.Column(db.String)
    filepath = db.Column(db.String)
    file_size = db.Column(db.String)
    original_created = db.Column(db.DateTimet(timezone=True))
    filehash = db.Column(db.String(64), unique=True) # Used to prevent duplicates