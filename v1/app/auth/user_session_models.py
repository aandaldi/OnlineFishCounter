from app import db

class UserSessionModel(db.Model):
    __tablename__ = 'user_session'
    uuid = db.Column(db.String(50), primary_key=True)