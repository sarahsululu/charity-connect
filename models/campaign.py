from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey, Numeric
from decimal import Decimal
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from models.database import Base
class Campaign(Base):
    __tablename__ = 'campaigns'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    goal_amount = Column(Numeric(10, 2), nullable=False)
    current_amount = Column(Numeric(10, 2), default=0.00)
    category = Column(String(100), nullable=False)
    start_date = Column(DateTime(timezone=True), server_default=func.now())
    end_date = Column(DateTime(timezone=True), nullable=True)
    is_active = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)
    image_url = Column(String(500), nullable=True)
    organization_name = Column(String(200), nullable=False)
    beneficiary_info = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    creator_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    creator = relationship("User", back_populates="campaigns")
    donations = relationship("Donation", back_populates="campaign", cascade="all, delete-orphan")
    
    @property
    def progress_percentage(self):
        """Calculate the percentage of goal achieved"""
        if self.goal_amount <= 0:
            return 0
        return min(float(self.current_amount / self.goal_amount * 100), 100)
    
    @property
    def remaining_amount(self):
        """Calculate remaining amount to reach goal"""
        return max(self.goal_amount - self.current_amount, 0)
    
    @property
    def is_completed(self):
        """Check if campaign has reached its goal"""
        return self.current_amount >= self.goal_amount
    
    @property
    def donation_count(self):
        """Get the number of donations for this campaign"""
        return len(self.donations)
    
    def add_donation(self, amount):
        """Add to current amount (called when a donation is made)"""
        self.current_amount = (self.current_amount or 0) + amount
    
    @property
    def status(self):
        """Get campaign status"""
        if not self.is_active:
            return "Inactive"
        elif self.is_completed:
            return "Completed"
        elif self.end_date and self.end_date < func.now():
            return "Expired"
        else:
            return "Active"
    
    def __repr__(self):
        return f"<Campaign {self.title}>"