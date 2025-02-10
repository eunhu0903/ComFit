from sqlalchemy import Column, String, Integer, Text
from sqlalchemy.orm import relationship
from db.session import Base

class Commit(Base):
    __tablename__="commit"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(50), nullable=False)
    duration = Column(Integer, nullable=False)
    sets = Column(Integer, nullable=False)
    intensity = Column(String, nullable=False)
    notes = Column(Text, nullable=True)

    user = relationship("User", back_populates="commit")

