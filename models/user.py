from models.base import Base
from sqlalchemy import DateTime, Integer, String, Text, func
from sqlalchemy.orm import mapped_column,relationship, backref
from sqlalchemy.sql import func

from flask_login import UserMixin
import bcrypt

class User(Base, UserMixin):
    __tablename__ = 'users'

    id  = mapped_column(Integer, primary_key=True, autoincrement=True)
    email = mapped_column(String(100), nullable=False)
    name  = mapped_column(String(100), nullable=False)
    password = mapped_column(String(100), nullable=False)
    created_at  = mapped_column(DateTime(timezone=True),server_default=func.now())
    role = mapped_column(String(100), nullable=True)


    def __repr__(self):
        return f'<User {self.name}>'
    
    def set_password(self, password):
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

