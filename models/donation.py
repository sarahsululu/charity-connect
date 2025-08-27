from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from models.database import Base

class Donation(Base):
    __tablename__ = 'donations'

    id = Column(Integer, primary_key=True)  # <- this is required!
    donor_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    campaign_id = Column(Integer, ForeignKey('campaigns.id'), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    message = Column(Text, nullable=True)
    is_anonymous = Column(Boolean, default=False)
    payment_method = Column(String(50), default='card')
    transaction_id = Column(String(100), unique=True, nullable=True)
    status = Column(String(20), default='completed')
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    donor = relationship("User", back_populates="donations")
    campaign = relationship("Campaign", back_populates="donations")

    @property
    def donor_name(self):
        if self.is_anonymous:
            return "Anonymous"
        return self.donor.full_name if self.donor else "Unknown"

    @property
    def is_successful(self):
        return self.status == 'completed'

    def __repr__(self):
        return f"<Donation ${self.amount} to {self.campaign.title if self.campaign else 'Unknown'}>"
