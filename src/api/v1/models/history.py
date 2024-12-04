from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from ..database import Base


class History(Base):
    __tablename__ = "histories"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String, nullable=True)
    longitude = Column(Float, nullable=True)
    latitude = Column(Float, nullable=True)
    temperature = Column(Float)
    description = Column(String)
    created_at = Column(DateTime)
    created_by_id = Column(Integer, ForeignKey("users.id"))
    created_by = relationship("User", back_populates="history")
