from app import db

class LOG(db.Model):
    __tablename__ = 'log'
    id = db.Column(db.Integer, primary_key = True,unique = True)
    ip = db.Column(db.String(255))
    address = db.Column(db.String(255))
    #timestamp = db.Column(db.DateTime)
    url = db.Column(db.String(255))
    status = db.Column(db.String(255))
    num = db.Column(db.Integer)

    def __repr__(self):
        return '<LOG table>'