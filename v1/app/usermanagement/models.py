from app import db
from datetime import datetime
from uuid import uuid4


class UsermanagementModel(db.Model):
    __tablename__ = 'usermanagement'

    uuid = db.Column(db.String(30), primary_key=True)
    username = db.Column(db.String(50), nullable=False, )
    password = db.Column(db.String(100), nullable=False, )
    roles = db.Column(db.String(64))
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    created_by = db.Column(db.String(64))
    date_modified = db.Column(db.DateTime, nullable=False)
    modified_by = db.Column(db.String(64))
    last_login = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean(), default=True)

    user_session_models = db.relationship('UserSessionModel', lazy='select',
                                          backref=db.backref('usermanagement', lazy='joined'))
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.uuid = str(uuid4())


    def __repr__(self):
        return "User {} ".format(self.username)

    def to_json(self):
        return {
            "uuid": self.uuid,
            "username": self.username,
            "roles": self.roles,
            "created_by": self.created_by,
            "created_at": self.date_created,
            "modified_by": self.modified_by,
            "modified_at": self.date_modified,
            "last_login": self.last_login,
            "is_active": self.is_active

        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def update_on_db(self):
        db.session.commit()

    @classmethod
    def lookup(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def identify(cls, uuid):
        return cls.query.filter_by(uuid=uuid).one_or_none()

    @property
    def identity(self):
        return self.uuid

    # @property
    # def is_valid(self):
    #     return self.is_active

    @property
    def rolenames(self):
        try:
            return self.roles.split(',')
        except Exception:
            return []
