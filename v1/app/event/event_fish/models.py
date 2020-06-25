from app import db
from datetime import datetime as dt
from uuid import uuid4

class EventFishModel(db.Model):
    __tablename__ = 'event_fish'
    uuid = db.Column(db.String(30), primary_key=True)
    date_created = db.Column(db.DateTime, nullable=False, default=dt.utcnow)
    created_by = db.Column(db.String(64))
    date_modified = db.Column(db.DateTime, nullable=False)
    modified_by = db.Column(db.String(64))
    stick_number = db.Column(db.Integer())
    fish_weight = db.Column(db.Float)
    usermanagement_uuid = db.Column(db.String(30), db.ForeignKey('usermanagement.uuid'))
    event_uuid = db.Column(db.String(30), db.ForeignKey('event.uuid'))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.uuid = str(uuid4())

    def __repr__(self):
        return "event {}".format(self.stick_number)

    def to_json(self):
        return {
            'uuid': self.uuid,
            'date_created': self.date_created,
            'created_by': self.created_by,
            'date_modified': self.date_modified,
            'modified_by': self.modified_by,
            'event_uuid': self.event_uuid,
            'fish_weight': self.fish_weight,
            'usermanagement_uuid': self.usermanagement_uuid,
            'stick_number': self.stick_number

        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def update_on_db(self):
        db.session.commit()

    @classmethod
    def lookup_by_usermanagement_id(cls, usermanagement_uuid):
        return cls.query.filter_by(usermanagement_uuid=usermanagement_uuid).first()

    @classmethod
    def lookup_by_event_id(cls, event_uuid):
        return cls.query.filter_by(event_uuid=event_uuid).first()

    @classmethod
    def lookup_by_id(cls, id):
        return cls.query.filter_by(uuid=id).first()