import uuid
from ..database.database import Base
from sqlalchemy import Column, String, TIMESTAMP, text, Enum
from sqlalchemy.dialects.postgresql import UUID 
from vanilla.pkg.schemas.user_schema import UserRole

class User(Base):
  __tablename__ = "users"

  id = Column(UUID(as_uuid=True),primary_key=True,nullable=False, default=uuid.uuid4)
  username = Column(String,nullable=False)
  email = Column(String,nullable=False)
  password = Column(String,nullable=False)
  role = Column(Enum(UserRole, name="user_role"), nullable=False)
  created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))