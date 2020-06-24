from app import db
from datetime import datetime as dt
from uuid import uuid4


class EventModel(db.Model):
    __tablename__ = 'event'
    uuid = db.Column(db.String(30), primary_key=True)
    date_created = db.Column(db.DateTime, nullable=False, default=dt.utcnow)
    created_by = db.Column(db.String(64))
    date_modified = db.Column(db.DateTime, nullable=False)
    modified_by = db.Column(db.String(64))
    name = db.Column(db.String(20))
    date = db.Column(db.DateTime)
    max_stick = db.Column(db.Integer())

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.uuid = str(uuid4())

    def __repr__(self):
        return "{}".format(self.name)


    def to_json(self):
        return {
            'uuid': self.uuid,
            'date_created': self.date_created,
            'created_by': self.created_by,
            'date_modified': self.date_modified,
            'modified_by': self.modified_by,
            'name': self.name,
            'date': self.date,
            'max_stick': self.max_stick

        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def update_on_db(self):
        db.session.commit()


    @classmethod
    def lookup(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def lookup_by_id(cls,id):
        return cls.query.filter_by(uuid=id).first()

