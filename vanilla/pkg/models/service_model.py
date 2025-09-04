from vanilla.pkg.database.database import Base
from sqlalchemy import Column, String, TIMESTAMP, text, ARRAY
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Service(Base):
  __tablename__ = "services"

  id = Column(UUID(as_uuid=True),primary_key=True,nullable=False, default=uuid.uuid4)
  service_name = Column(String, nullable=False)
  facility_name = Column(String,nullable=False)
  list_doctor = Column(ARRAY(String),nullable=False)
  created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))