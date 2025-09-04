from vanilla.pkg.database.database import Base
from sqlalchemy import Column, String, TIMESTAMP, text, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
import uuid
import enum

class AppointmentStatus(enum.Enum):
    scheduled = "scheduled"
    completed = "completed"
    cancelled = "cancelled"

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    doctor_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    service_id = Column(UUID(as_uuid=True), ForeignKey("services.id"), nullable=False)

    appointment_time = Column(TIMESTAMP(timezone=True), nullable=False)
    status = Column(Enum(AppointmentStatus), nullable=False, default=AppointmentStatus.scheduled)
    notes = Column(String, nullable=True)

    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
