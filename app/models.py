from sqlalchemy import Column,Integer,String,Date

from app.database import Base



class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True, nullable=False)
    last_name = Column(String, index=True, nullable=False)
    username = Column(String, index=True, nullable=True)
    company_name = Column(String, index=True, nullable=True)
    email = Column(String, index=True, nullable=True)
    password = Column(String, nullable=True)
    mob = Column(String, nullable=True)
    hashtag = Column(String, nullable=True)
    date_of_birth = Column(String, nullable=True)
    project_id = Column(String, index=True, nullable=True)