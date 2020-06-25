from app import db
from uuid import uuid4


class UserSessionModel(db.Model):
    __tablename__ = 'user_session'
    uuid = db.Column(db.String(50), primary_key=True)
    access_token = db.Column(db.String(100))
    usermanagement_uuid = db.Column(db.String(30), db.ForeignKey('usermanagement.uuid'))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.uuid = str(uuid4())

    def __repr__(self):
        return "User {} session models".format(self.usermanagement_uuid)

    @classmethod
    def lookup(cls, usermanagement_uuid):
        return cls.query.filter_by(usermanagement_uuid=usermanagement_uuid).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
