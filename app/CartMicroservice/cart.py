from setup_app import db
from sqlalchemy import Column, Integer, DateTime, String, Boolean, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship,backref


class Cart(db.Model):
    __tablename__ = 'cart'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=False, nullable=False)

    item = Column(String(256), unique=False, nullable=False)
    price = Column(String(256), unique=False, nullable=False)
    qty = Column(String(256), unique=False, nullable=False)



    def __repr__(self):
        return 'id: '.join([str(id)])

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)