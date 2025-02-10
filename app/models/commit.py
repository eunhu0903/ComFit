from sqlalchemy import Column, String, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import ENUM
from db.session import Base

class Commit(Base):
    __tablename__="commit"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(50), nullable=False)
    duration = Column(Integer, nullable=False)
    sets = Column(Integer, nullable=False)
    intensity = Column(ENUM('LOW', 'MEDIUM', 'HIGH', name='intensity_enum'))
    memo = Column(Text, nullable=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="commit")

