from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from app.db.base import Base
import datetime
import enum

class UserRole(str, enum.Enum):
    OWNER = "owner"
    COLLABORATOR = "collaborator"

class EditingSession(Base):
    __tablename__ = "editing_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    code_file_id = Column(Integer, ForeignKey("code_files.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    role = Column(Enum(UserRole))
    cursor_position = Column(Integer)
    last_active = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="editing_sessions")
    code_file = relationship("CodeFile", back_populates="editing_sessions") 