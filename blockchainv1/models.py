from blockchainv1 import db
import datetime


class BlocksDB(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, nullable=False, default= datetime.datetime.utcnow)
    blocks = db.Column(db.String(500), unique=True, nullable=False)

    def __repr__(self):
        return f'<User: {self.blocks}>'



