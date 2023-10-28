from . import db
from sqlalchemy.sql import func
import uuid


class Data(db.Model):
    id = db.Column(db.String(1000), primary_key=True, default=lambda: str(uuid.uuid4()))
    data = db.Column(db.Text())
    date = db.Column(db.DateTime(timezone=True), default=func.now())